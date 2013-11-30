from __future__ import print_function
import ConfigParser
import os

def get_session(session_name):
  session = ConfigParser.ConfigParser()
  file_name = os.path.join("sessions", session_name)
  with open(file_name, "r") as fp:
    session.readfp(fp)
  return session

def get_session_list():
  sessions = {}
  for root, dirnames, files in os.walk("sessions"):
    for fname in files:
      print("reading {}".format(fname))
      sessions[fname] = ConfigParser.ConfigParser()
      with open(os.path.join(root, fname), "r")as fp:
        sessions[fname].readfp(fp)
  return sessions

def sort_sessions_by_deadline(sessions):
  # TODO: add sorting by time
  return sessions
