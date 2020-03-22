import sys, os, time
C = os.path.abspath(os.path.dirname(__file__))

from flask import Flask

app = Flask(__name__)

# schedule
import schedule
from threading import Thread

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


sched = Thread(target=run_schedule, daemon=True)
sched.start()

