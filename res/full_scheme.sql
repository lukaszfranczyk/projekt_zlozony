CREATE TABLE users (
    id integer PRIMARY KEY,
    name varchar(255) NOT NULL,
    password varchar(128) NOT NULL,
    CONSTRAINT name UNIQUE(name)
);