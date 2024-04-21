CREATE TABLE films (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    length TEXT,
    genre TEXT,
    director TEXT,
    writer TEXT,
    created_at TIMESTAMP
);

CREATE TABLE film_visible (
    id SERIAL PRIMARY KEY,
    titleVisible BOOLEAN,
    descriptionVisible BOOLEAN,
    lengthVisible BOOLEAN,
    genreVisible BOOLEAN,
    directorVisible BOOLEAN,
    writerVisible BOOLEAN,
    created_atVisible BOOLEAN,
    films_id INTEGER REFERENCES films ON DELETE CASCADE
);


CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    films_id INTEGER REFERENCES films ON DELETE CASCADE,
    rating INTEGER,
    message TEXT,
    sent_at TIMESTAMP
);


CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT,
    isAdmin BOOLEAN
);