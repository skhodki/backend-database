# Skhodka Backend 🚀

REST API for a meetup and event discovery application based on shared interests. The backend provides user registration, event creation, and smart matching based on shared tags and hobbies.

## Prerequisites
Before you begin, ensure you have the following installed on your computer:
1. **Python 3.11+**
2. **PostgreSQL** (with pgAdmin or any other database GUI)

---

## 🛠 Step-by-Step Setup Guide (For Frontend Devs & Reviewers)

Follow these steps to run the backend server and database locally on your machine.

### Step 1: Clone the repository
Open your terminal and clone this project:
```bash
git clone [https://github.com/skhodki/backend-database.git](https://github.com/skhodki/backend-database.git)
cd skhodka_backend
Step 2: Set up the Database (PostgreSQL)
Open pgAdmin (or your preferred PostgreSQL client).

Create a new empty database and name it skhodka.

Open the Query Tool for this new database.

Copy the entire SQL code from the schema.sql file (located in this repository) and execute it. This will create all the necessary tables.

Step 3: Configure Environment Variables
The application needs to know how to connect to your local database.

In the root folder of the project, create a new file named exactly .env (don't forget the dot at the beginning).

Copy the following text into it, and replace your_postgres_password with your actual PostgreSQL password:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=skhodka
DB_USER=postgres
DB_PASSWORD=your_postgres_password
Step 4: Install Dependencies
Open the terminal in the project folder and run:

Bash
pip install -r requirements.txt
Step 5: Start the Server
Run the following command to start the FastAPI server:

Bash
uvicorn main:app --reload
API Documentation
Once the server is running, you don't need to read the Python code. You can find the full interactive API documentation, endpoints, and JSON schemas here:

http://127.0.0.1:8000/docs

You can use these endpoints in your frontend code (using fetch or axios) pointing to http://127.0.0.1:8000/....