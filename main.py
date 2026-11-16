from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from database import get_db_connection
from psycopg2.extras import RealDictCursor
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="Skhodka API", description="Backend for finding interest-based meetups and events")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EventCreate(BaseModel):
    title: str
    description: str
    location_id: int
    event_date: datetime
    min_participants: int = 2
    max_participants: int = 10
    creator_id: int

class JoinEvent(BaseModel):
    user_id: int

@app.get("/users")
def get_all_users():
    """Получить список всех пользователей"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                SELECT u.username, u.email, u.city
                FROM users u;
            """
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as u:
        raise HTTPException(status_code=500, detail=str(u))
    finally:
        conn.close()

@app.get("/events")
def get_all_events():
    """Получить список всех сходок"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                SELECT e.event_id, e.title, e.event_date, e.status, l.name AS location_name
                FROM events e
                LEFT JOIN locations l ON e.location_id = l.location_id;
            """
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.post("/events")
def create_event(event: EventCreate):
    """Создать новую сходку"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO events (title, description, location_id, event_date, min_participants, max_participants, creator_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING event_id;
            """
            cursor.execute(query, (
                event.title, event.description, event.location_id,
                event.event_date, event.min_participants, event.max_participants, event.creator_id
            ))
            new_event_id = cursor.fetchone()[0]

            conn.commit()
            return {"message": "Event successfully created!", "event_id": new_event_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.post("/events/{event_id}/join")
def join_event(event_id: int, join_data: JoinEvent):
    """Записаться на сходку"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                INSERT INTO event_participants (event_id, user_id)
                VALUES (%s, %s)
                ON CONFLICT (event_id, user_id) DO NOTHING;
            """, (event_id, join_data.user_id))

            cursor.execute("""
                SELECT e.min_participants, COUNT(ep.user_id) as current_count
                FROM events e
                LEFT JOIN event_participants ep ON e.event_id = ep.event_id
                WHERE e.event_id = %s
                GROUP BY e.event_id;
            """, (event_id,))

            result = cursor.fetchone()

            if result and result['current_count'] >= result['min_participants']:
                cursor.execute("""
                    UPDATE events SET status = 'confirmed' WHERE event_id = %s;
                """, (event_id,))

            conn.commit()
            return {
                "message": "Successfully joined!",
                "current_participants": result['current_count'],
                "required": result['min_participants']
            }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/events/match/{user_id}")
def get_matching_events(user_id: int):
    """Подобрать сходки по интересам"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                SELECT DISTINCT e.event_id, e.title, e.event_date, e.status, l.name AS location_name
                FROM events e
                JOIN event_interests ei ON e.event_id = ei.event_id
                JOIN user_interests ui ON ei.interest_id = ui.interest_id
                LEFT JOIN locations l ON e.location_id = l.location_id
                WHERE ui.user_id = %s AND e.status != 'cancelled';
            """
            cursor.execute(query, (user_id,))
            matched_events = cursor.fetchall()

            if not matched_events:
                return {"message": "No matching events found yet, but you can create your own!"}

            return matched_events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# Ensure that a request for "/" serves up "public/index.html"
app.mount("/", StaticFiles(directory=Path("public"), html=True))