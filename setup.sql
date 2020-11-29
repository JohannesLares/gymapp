CREATE TABLE users (user_id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, email TEXT UNIQUE NOT NULL, created_on TIMESTAMP NOT NULL, last_login TIMESTAMP, admin BOOLEAN DEFAULT 'f');

CREATE TABLE moves (move_id SERIAL PRIMARY KEY, name TEXT NOT NULL, public BOOLEAN DEFAULT 'f', user_id INTEGER NOT NULL, description TEXT, CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(user_id));

CREATE TABLE set (
    set_id SERIAL PRIMARY KEY, 
    user_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    move_id INTEGER NOT NULL,
    description TEXT,
    place INT,
    weight INT,
    time TIMESTAMP,
    reps INT,
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
            REFERENCES users(user_id),
    CONSTRAINT fk_move
        FOREIGN KEY(move_id)
            REFERENCES moves(move_id),
    CONSTRAINT fk_plan
        FOREIGN KEY(plan_id)
            REFERENCES plans(plan_id)
);

CREATE TABLE plans (
    plan_id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    user_id INT NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
            REFERENCES users(user_id)
);