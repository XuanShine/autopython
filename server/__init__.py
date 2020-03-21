import sys
import os
import time

C = os.path.abspath(os.path.dirname(__file__))


from flask import Flask
from .pyaccess_server import pyaccess

app = Flask(__name__)

app.register_blueprint(pyaccess)


import schedule
from threading import Thread

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


sched = Thread(target=run_schedule, daemon=True)
sched.start()

