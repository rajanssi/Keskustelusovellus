CREATE TABLE Boards (
    id SERIAL PRIMARY KEY,
    boardname TEXT
    );

CREATE TABLE Users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT NOT NULL, 
    role INTEGER DEFAULT 1
    );

CREATE TABLE Threads(
    id SERIAL PRIMARY KEY, 
    board_id INTEGER REFERENCES boards, 
    user_id INTEGER REFERENCES users,
    title TEXT NOT NULL,
    opening_message TEXT NOT NULL,
    created_at TIMESTAMP
    );
    
CREATE TABLE Comments (
    id SERIAL PRIMARY KEY, 
    user_id INTEGER REFERENCES users,
    thread_id INTEGER REFERENCES threads,
    content TEXT NOT NULL, 
    created_at TIMESTAMP,
    visible INTEGER DEFAULT 1
    );

CREATE TABLE PrivateBoards(
    id SERIAL PRIMARY KEY,
    boardname TEXT
    );

CREATE TABLE PrivateBoardUsers (
    board_id INTEGER REFERENCES PrivateBoards,
    user_id INTEGER REFERENCES users
    );