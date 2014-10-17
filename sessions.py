from __future__ import print_function

class Session(object):
    def __init__(self, id, place_id, deadline):
        self.id = id
        self.place_id = id
        self.place_name = id
        self.deadline = deadline

def get_session_list():
    s1 = Session("adsf", "chommi", "11:30")
    return [s1]

def pizza_places():
    """Returns list of available pizza places

    :returns: list of touples (place_name, place_id)
    """
    return ["Carla"]

def create_session(session_name, data):
    pass

def add_order_to_session(form):
    pass

def load_session(session_name):
    pass

def save_session(session_name, session):
    pass

def sort_sessions_by_deadline(sessions):
    pass
