from __future__ import print_function
from pizza import query_db, sql_query

def get_session_list():
    sessions = query_db("select * from sessions;")
    return sessions

def get_session(session_id):
    session = {}
    query = "select email, extra, session, pizza, id from orders where session == '{}';".format(session_id)
    orders = query_db(query)
    session["orders"] = []
    for order in orders:
        o = {
                "email" : order[0],
                "extra" : order[1],
                "session" : order[2],
                "pizza" : order[3],
                "id" : order[4]
            }
        query = "select name, price from pizzas where id == '{}'".format(o["pizza"])
        pizza = query_db(query, one=True)
        o["pizza_name"] = pizza[0]
        o["pizza_price"] = pizza[1]

        session["orders"].append(o)

    return session



def pizza_places():
    """Returns list of available pizza places

    :returns: list of pizzaplaces (name, url)
    """
    places = query_db("select * from pizzaplaces;")
    return places

def pizzas(session_id):
    pizzaplace = query_db("select pizzaplace from sessions where id == '{}';".format(session_id), one=True)
    if pizzaplace is None:
        return
    pizzas = query_db("select * from pizzas where pizzaplace == lower('{}');".format(pizzaplace[0]))
    return pizzas

def create_session(email, data):
    pizza_place_id = data["pizza_place"]
    deadline = data["deadline"].strftime("%Y-%m-%d %H:%M")
    query = "insert into sessions (email, deadline, pizzaplace) values ('{}','{}', '{}');"
    query = query.format(email, deadline, pizza_place_id)
    sql_query(query)
    session_id = query_db("select (id) from sessions where email == '{}'".format(email), one=True)
    return session_id[0]

def add_order(session_id, user_email, pizza_id, extra):
    query = "insert into orders (email, session, pizza, extra) values ('{}', '{}', '{}', '{}');"
    query = query.format(user_email, session_id, pizza_id, extra)
    sql_query(query)

    order_id = query_db("select (id) from orders where email == '{}'".format(user_email), one=True)
    print(order_id)
    return order_id[0]

def delete_order(order_id):
    query = "delete from orders where id == '{}'".format(order_id)
    sql_query(query)
    print("order {} was deleted".format(order_id))

def get_order(session_id, user_email):
    order = {}
    query = "select pizza from orders where email == '{}' AND session == '{}'"
    query = query.format(user_email, session_id)
    pizza_id = query_db(query, one=True)
    # get id from tuple
    pizza_id = pizza_id[0]
    query = "select name, price from pizzas where id == '{}'".format(pizza_id)
    pizza = query_db(query, one=True)
    print("Pizza {} for {}euro".format(pizza[0], pizza[1]))
    order["pizza"] = pizza[0]
    order["price"] = pizza[1]
    return order

