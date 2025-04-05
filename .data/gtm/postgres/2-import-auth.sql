CREATE DATABASE auth;

\c auth;

CREATE TABLE users
  (
    id             SERIAL,
    email          VARCHAR(255),
    password       VARCHAR(64),
    roles          VARCHAR(64),
    created_at     TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
  );

CREATE UNIQUE INDEX email
  ON users(email);

\COPY users FROM '/docker-entrypoint-initdb.d/auth_users.csv' WITH (FORMAT csv, HEADER true);
