CREATE DATABASE emergent_auth;

\c emergent_auth;

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

INSERT INTO public.users (id, email, password, roles) VALUES
	(1, 'adam.mcdaniel@bigpond.com', '$2a$10$DSRHAPZP0fuEFioGOPOdW.kgFWZvQgmMihaBYsUs8rO4cdHFFK7cS', 'customer'),
	(2, 'daniel.lane@yahoo.com.au', '$2a$10$DSRHAPZP0fuEFioGOPOdW.kgFWZvQgmMihaBYsUs8rO4cdHFFK7cS', 'customer'),
	(3, 'nathan.moore@outlook.com.au', '$2a$10$DSRHAPZP0fuEFioGOPOdW.kgFWZvQgmMihaBYsUs8rO4cdHFFK7cS', 'customer'),
  (4, 'katherine.arellano@gmail.com', '$2a$10$DSRHAPZP0fuEFioGOPOdW.kgFWZvQgmMihaBYsUs8rO4cdHFFK7cS', 'customer'),
	(5, 'jason.willis@hotmail.com.au', '$2a$10$DSRHAPZP0fuEFioGOPOdW.kgFWZvQgmMihaBYsUs8rO4cdHFFK7cS', 'customer'),
	(6, 'mark.holland@yahoo.com.au', '$2a$10$DSRHAPZP0fuEFioGOPOdW.kgFWZvQgmMihaBYsUs8rO4cdHFFK7cS', 'customer'),
  (7, 'alexis.smith@gmail.com', '$2a$10$DSRHAPZP0fuEFioGOPOdW.kgFWZvQgmMihaBYsUs8rO4cdHFFK7cS', 'customer'),
	(8, 'tiffany.ayers@gmail.com', '$2a$10$DSRHAPZP0fuEFioGOPOdW.kgFWZvQgmMihaBYsUs8rO4cdHFFK7cS', 'customer'),
	(9, 'matthew.reed@bigpond.com', '$2a$10$DSRHAPZP0fuEFioGOPOdW.kgFWZvQgmMihaBYsUs8rO4cdHFFK7cS', 'customer'),
	(10, 'isaac.kramer@holotel.xyz', '$2a$10$DSRHAPZP0fuEFioGOPOdW.kgFWZvQgmMihaBYsUs8rO4cdHFFK7cS', 'support');

SELECT setval('public.users_id_seq', COALESCE((SELECT MAX(id)+1 FROM public.users), 1), false);
