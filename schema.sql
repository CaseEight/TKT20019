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

-- default films for testing

INSERT INTO films (title, description, length, genre, director, writer, created_at) VALUES ('Kummisetä', 'Eeppinen rikoselokuva', '175', 'rikos', 'Francis Ford Coppola', 'Mario Puzo', '2024-04-05 20:23:54');
INSERT INTO films (title, description, length, genre, director, writer, created_at) VALUES ('Havumetsän lapset', 'Taidokas dokumentti elokapinan hahmoista', '93', 'dokumentti', 'Virpi Suutari', 'Virpi Suutari', '2024-04-05 20:24:54');

INSERT INTO film_visible (titleVisible, descriptionVisible, lengthVisible, genreVisible, directorVisible, writerVisible, created_atVisible, films_id) VALUES (true,true,true,true,true,true,true,1);
INSERT INTO film_visible (titleVisible, descriptionVisible, lengthVisible, genreVisible, directorVisible, writerVisible, created_atVisible, films_id) VALUES (true,true,true,true,true,true,true,2);