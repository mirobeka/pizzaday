CREATE TABLE sessions(
  id INTEGER PRIMARY KEY,
  deadline DATETIME,
  pizzaplace INTEGER
);

CREATE TABLE pizzaplaces(
  id INTEGER PRIMARY KEY,
  name TEXT,
  url TEXT
);

CREATE TABLE pizzas(
  id INTEGER PRIMARY KEY,
  name TEXT,
  price REAL,
  pizzaplace INTEGER,
  FOREIGN KEY(pizzaplace) REFERENCES pizzaplaces(id)
);

CREATE TABLE orders(
  id INTEGER PRIMARY KEY,
  mail TEXT,
  extra TEXT,
  session INTEGER,
  pizza INTEGER,
  FOREIGN KEY(session) REFERENCES sessions(id),
  FOREIGN KEY(pizza) REFERENCES pizzas(id)
);
