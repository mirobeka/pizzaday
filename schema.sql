CREATE TABLE sessions(
  id INTEGER PRIMARY KEY,
  email TEXT,
  deadline DATETIME,
  pizzaplace TEXT,
  FOREIGN KEY(pizzaplace) REFERENCES pizzaplaces(name)
);

CREATE TABLE pizzaplaces(
  name TEXT PRIMARY KEY,
  url TEXT
);


CREATE TABLE pizzas(
  id INTEGER PRIMARY KEY,
  name TEXT,
  price REAL,
  pizzaplace TEXT,
  FOREIGN KEY(pizzaplace) REFERENCES pizzaplaces(name)
);


CREATE TABLE orders(
  id INTEGER PRIMARY KEY,
  email TEXT,
  extra TEXT,
  session INTEGER,
  pizza INTEGER,
  FOREIGN KEY(session) REFERENCES sessions(id),
  FOREIGN KEY(pizza) REFERENCES pizzas(id)
);


INSERT INTO pizzaplaces (name, url) VALUES ("carla", "http://www.pizzacarla.sk/");
INSERT INTO pizzaplaces (name, url) VALUES ("chommi", "http://www.chommi.sk/pizza.html");
INSERT INTO pizzaplaces (name, url) VALUES ("erik", "http://pizzaerik.sk/");

INSERT INTO pizzas (id, name, price, pizzaplace) VALUES ("1", "Margeritha", "4.20", "carla");
INSERT INTO pizzas (id, name, price, pizzaplace) VALUES ("2", "Roma", "6.90", "carla");
INSERT INTO pizzas (id, name, price, pizzaplace) VALUES ("3", "Margeritha erik", "4.20", "erik");
INSERT INTO pizzas (id, name, price, pizzaplace) VALUES ("4", "Margeritha chommi", "4.20", "chommi");

INSERT INTO sessions (id, email, deadline, pizzaplace) VALUES ("1", "mirobeka@gmail.com", "2015-01-13 10:00", "carla");

INSERT INTO orders (id, email, extra, session, pizza) VALUES ("1", "lala@gmail.com", "Vajice naviac", "1", "2");
