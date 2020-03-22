import sys, os, time
C = os.path.abspath(os.path.dirname(__file__))

from flask import Flask
from .pyaccess_server import pyaccess
from .pywubook_sever import pywubook

app = Flask(__name__)
app.register_blueprint(pyaccess)
app.register_blueprint(pywubook)


# schedule
import schedule
from threading import Thread

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


sched = Thread(target=run_schedule, daemon=True)
sched.start()

