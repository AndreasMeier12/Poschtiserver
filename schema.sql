DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS command;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);


CREATE TABLE command (
    command_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    list_id INTEGER NOT NULL,
    origin TEXT NOT NULL,
    name TEXT NOT NULL,
    quantity TEXT NOT NULL,
    shop NOT NULL,
    timestamp INTEGER


);
