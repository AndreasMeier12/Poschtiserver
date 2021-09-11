DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS shoppingitem;
DROP TABLE IF EXISTS shoppinglist;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);


CREATE TABLE shoppingitem (
  item_key INTEGER PRIMARY KEY AUTOINCREMENT,
  userid INTEGER NOT NULL,
  listkey INTEGER NOT NULL,
  name TEXT NOT NULL,
  quantity TEXT NOT NULL,
  shop TEXT
);

CREATE TABLE shoppinglist (
  listkey INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER NOT NULL,
  name TEXT NOT NULL
);
