import sys, os, time
C = os.path.abspath(os.path.dirname(__file__))
import requests
import socket

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

MAIN_IP = "10.0.0.15"

db = SQLAlchemy()

######################################
#### Application Factory Function ####
######################################

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///list_rpi.db"

    return app

    
##########################
#### Helper Functions ####
##########################

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)


# schedule
import schedule
from threading import Thread

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


sched = Thread(target=run_schedule, daemon=True)
sched.start()


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def send_ip():
    """ Send identity to the main RPI """
    with open(os.path.join(C, "..", "..", "RPI_ID"), "r") as f_in:
        identity = f_in.read().strip()
    self_ip = get_ip()
    link = f"http://{MAIN_IP}:5000/register_ip/{self_ip}/{identity}"
    r = requests.get(link)
    return r

# schedule.every().day.do(send_ip)