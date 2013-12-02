from __future__ import print_function
import ConfigParser
import os

def get_session(session_name):
  session = load_session(session_name)
  return session

def get_session_list():
  if exists_or_create_session_folder():
    sessions = {}
    for root, dirnames, files in os.walk("sessions"):
      for session_name in files:
        sessions[session_name] = load_session(session_name)
    return sessions
  return {}

def create_session(session_name, data):
  session = ConfigParser.ConfigParser()
  session.add_section("info")
  session.add_section("orders")
  session.add_section("extra")
  session.add_section("size")

  session.set("info", "deadline", data["deadline"])
  session.set("info", "restaurant", data["restaurant"])
  session.set("info", "approx_lunch", data["approx_lunch"])
  session.set("info", "recipients", data["recipients"])

  save_session(session_name, session)

def add_order_to_session(session_name, order):
  session = load_session(session_name)
  session.set("orders", order["name"], order["pizza"])
  session.set("size", order["name"], order["size"])
  if "extra" in order:
    session.set("extra", order["name"], order["extra"])

  save_session(session_name, session)

def load_session(session_name):
  if exists_or_create_session_folder():
    session = ConfigParser.ConfigParser()
    file_path = os.path.join("sessions", session_name)
    with open(file_path, "r") as fp:
      session.readfp(fp)
    return session

def save_session(session_name, session):
  if exists_or_create_session_folder():
    file_path = os.path.join("sessions", session_name)
    if os.path.isfile(file_path):
      return False
    else:
      with open(file_path, "w") as fp:
        session.write(fp)
      return True
  return False

def exists_or_create_session_folder():
  if not os.path.isdir("sessions"):
    try:
      os.mkdir("sessions")
    except:
      print("failed to create sessions folder")
      return False
  return True

def sort_sessions_by_deadline(sessions):
  # TODO: add sorting by time
  return sessions
