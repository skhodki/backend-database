CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL,
    capacity INT, 
    description TEXT
);

CREATE TABLE interests (
    interest_id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    city VARCHAR(50),
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_interests (
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    interest_id INT REFERENCES interests(interest_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, interest_id)
);

CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    location_id INT REFERENCES locations(location_id) ON DELETE RESTRICT,
    event_date TIMESTAMP NOT NULL,
    min_participants INT DEFAULT 2,
    max_participants INT,
    status VARCHAR(20) DEFAULT 'gathering', 
    creator_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE event_interests (
    event_id INT REFERENCES events(event_id) ON DELETE CASCADE,
    interest_id INT REFERENCES interests(interest_id) ON DELETE CASCADE,
    PRIMARY KEY (event_id, interest_id)
);

CREATE TABLE event_participants (
    event_id INT REFERENCES events(event_id) ON DELETE CASCADE,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (event_id, user_id)
);

-- === TEST DATA (For frontend development) ===

-- 1. Insert a test location
INSERT INTO locations (name, address, capacity, description) 
VALUES ('Board Game Cafe "Zerno"', '15 Lenin Street', 20, 'Cozy place for board games');

-- 2. Insert base interests
INSERT INTO interests (name) 
VALUES ('Board Games'), ('Data Analysis'), ('English Speaking');

-- 3. Insert test users
INSERT INTO users (username, email, city) 
VALUES 
('Anya', 'anya@example.com', 'Moscow'),
('Ivan', 'ivan@example.com', 'Moscow');

-- 4. Link users to interests
-- Anya likes Data Analysis (2) and English (3)
INSERT INTO user_interests (user_id, interest_id) VALUES (1, 2), (1, 3);
-- Ivan likes Board Games (1) and English (3)
INSERT INTO user_interests (user_id, interest_id) VALUES (2, 1), (2, 3);