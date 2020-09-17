CREATE TABLE boards (
    id SERIAL PRIMARY KEY,
    boardname TEXT
    );

CREATE TABLE threads(
    id SERIAL PRIMARY KEY, 
    board_id INTEGER REFERENCES boards, 
    title TEXT, 
    created_at TIMESTAMP
    );

CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT, 
    role TEXT
    );

CREATE TABLE comments (
    id SERIAL PRIMARY KEY, 
    user_id INTEGER REFERENCES users, 
    content TEXT, 
    created_at TIMESTAMP
    );