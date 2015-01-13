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

INSERT INTO pizzas (name, price, pizzaplace) VALUES ("Margeritha", "4.20", "carla");
INSERT INTO pizzas (name, price, pizzaplace) VALUES ("Roma", "6.90", "Carla");
INSERT INTO pizzas (name, price, pizzaplace) VALUES ("Margeritha erik", "4.20", "erik");
INSERT INTO pizzas (name, price, pizzaplace) VALUES ("Margeritha chommi", "4.20", "chommi");
