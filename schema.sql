CREATE TABLE sessions(
  id integer primary key autoincrement not null,
  start datetime default current_timestamp,
  end datetime not null,
  approxarrival datetime,
  pizzaplace integer not null,
  foreign key(pizzaplace) references pizzaplaces(id),
);

CREATE TABLE pizzaplaces(
  id integer primary key autoincrement not null,
  name text not null,
  url text not null
);

CREATE TABLE pizzas(
  id integer primary key autoincrement not null,
  name text not null,
  size text not null,
  weight integer not null,
  price real not null,
  pizzaplace integer not null,
  image blob,
  foreign key(pizzaplace) references pizzaplaces(id)
);

CREATE TABLE orders(
  id integer primary key autoincrement not null,
  mail text not null,
  extra text,
  session integer not null,
  foreign key(session) references sessions(id),
  pizza integer not null,
  foreign key(pizza) references pizzas(id)
);
