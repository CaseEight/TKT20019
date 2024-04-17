CREATE TABLE elokuvat (
    id SERIAL PRIMARY KEY,
    nimi TEXT,
    kuvaus TEXT,
    kesto TEXT,
    genre TEXT,
    ohjaaja TEXT,
    kasikirjoittaja TEXT,
    created_at TIMESTAMP
);

CREATE TABLE choices (
    id SERIAL PRIMARY KEY,
    elokuvat_id INTEGER REFERENCES elokuvat,
    choice TEXT
);

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    elokuvat_id INTEGER REFERENCES elokuvat,
    rating INTEGER,
    message TEXT,
    sent_at TIMESTAMP
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    choice_id INTEGER REFERENCES choices,
    sent_at TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT
);