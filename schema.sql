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

CREATE TABLE film_visible (
    id SERIAL PRIMARY KEY,
    nimiVisible BOOLEAN,
    kuvausVisible BOOLEAN,
    kestoVisible BOOLEAN,
    genreVisible BOOLEAN,
    ohjaajaVisible BOOLEAN,
    kasikirjoittajaVisible BOOLEAN,
    created_atVisible BOOLEAN,
    elokuvat_id INTEGER REFERENCES elokuvat ON DELETE CASCADE
);


CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    elokuvat_id INTEGER REFERENCES elokuvat ON DELETE CASCADE,
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