CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role VARCHAR(50)
);
INSERT INTO users (first_name, last_name, role) VALUES ('Michal', 'Mucha', 'student');