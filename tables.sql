CREATE TABLE projects(
    id SERIAL PRIMARY KEY,
    projects_name VARCHAR(255) NOT NULL,
    discord_link VARCHAR(255) NOT NULL
);

CREATE TABLE result(
    id SERIAL PRIMARY KEY,
    projects_name VARCHAR(255) NOT NULL,
    login VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL
);