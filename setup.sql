CREATE TABLE users (user_id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, email TEXT UNIQUE NOT NULL, created_on TIMESTAMP NOT NULL, last_login TIMESTAMP);

CREATE TABLE moves (move_id SERIAL PRIMARY KEY, name TEXT NOT NULL, public BOOLEAN DEFAULT 'f', user_id INTEGER NOT NULL, description TEXT);