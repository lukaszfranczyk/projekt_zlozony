DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    first_name varchar(255),
    last_name varchar(255),
    login varchar(255) NOT NULL,
    password varchar(128) NOT NULL,
    email varchar(50),
    CONSTRAINT login UNIQUE(login)
);

CREATE TABLE board (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    message TEXT,
    add_date TIMESTAMP DEFAULT now()
)

GRANT ALL ON ALL TABLES IN SCHEMA PUBLIC TO portal_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA PUBLIC TO portal_user;