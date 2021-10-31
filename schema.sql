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
    timestamp INTEGER,
    foreign key (user_id) REFERENCES user(id),
    foreign key (list_id) REFERENCES list(list_id)
);

CREATE TABLE listcommand(
    command_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL ,
    list_id NOT NULL,
    origin TEXT NOT NULL
);

CREATE TABLE list(
    list_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user(id),
    PRIMARY KEY (user_id, list_id)

)