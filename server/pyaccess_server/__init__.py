# from flask import Blueprint
import schedule

# pyaccess = Blueprint("pyaccess", __name__, url_prefix="/pyaccess")

from .views import pyaccess

from PyAccess import lock_door

schedule.every().day.at(f"07:00").do(lock_door.open_door).tag("open_door")
schedule.every().day.at(f"22:00").do(lock_door.close_door).tag("close_door")
task_auto = schedule.every().hour.do(lock_door.main, 7, 22).tag("auto_door")
task_auto.run()

