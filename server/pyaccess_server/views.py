from flask import Flask, escape, request
from . import pyaccess

import schedule
import time
from threading import Thread

from PyAccess import lock_door
from PyAccess.lock_door import *


# schedule
tasks = dict()
hour_on_off = ["07", "22"]


@pyaccess.route("/help")
def help():
    return """/set_state/<state>/<wait_time> : state can be 'on' or 'off'
    "/get_state" 
    "/get_state_hour"
    "/set_state_hour/<state>/<string:hour>" : state : "on" or "off"; set new hour on or new hour off
    """

@pyaccess.route('/set_state/<state>/<wait_time>')
def set_state(state: str, wait_time=3600):
    """state can be 'on' or 'off' """
    if state == "on":
        open_door()
    else:
        close_door()
    schedule.clear("open_door")
    schedule.clear("close_door")
    schedule.clear("auto_door")

    def restart_jobs():
        # TODO: prendre en compte les modifications qui peuvent être faites pendant le temps de pause
        time.sleep(wait_time)
        schedule.every().day.at(f"{hour_on_off[0]}:00").do(open_door).tag("open_door")
        schedule.every().day.at(f"{hour_on_off[1]}:00").do(close_door).tag("close_door")
        task_auto = schedule.every().hour.do(lock_door.main, *hour_on_off) 
        task_auto.run()

    t2 = Thread(target=restart_jobs, daemon=True)
    t2.start()

@pyaccess.route("/get_state")
def get_state():
    return "open" if is_open() else "close"

@pyaccess.route("/set_state_hour/<state>/<string:hour>")
def set_state_hour(state, hour):
    """
    <state> : "on" "off" "auto" 
    <hour> : int, but is ignore if state == auto
    """
    if state == "auto":
        schedule.clear("open_door")
        schedule.clear("close_door")
        schedule.clear("auto_door")
        schedule.every().day.at(f"07:00").do(open_door).tag("open_door")
        schedule.every().day.at(f"22:00").do(close_door).tag("close_door")
        schedule.every().hour.do(lock_door.main, 7, 22).tag("auto_door")
    else:
        schedule.clear("auto_door")
        if state == "on":
            schedule.clear("open_door")
            hour_on_off[0] = hour
            tasks["on"] = schedule.every().day.at(f"{hour}:00").do(open_door).tag("open_door")
        elif state == "off":
            hour_on_off[1] = hour
            schedule.clear("close_door")
            schedule.every().day.at(f"{hour}:00").do(close_door).tag("close_door")
        
        task_auto = schedule.every().hour.do(lock_door.main, int(hour_on_off[0]), int(hour_on_off[1])).tag("auto_door")
        task_auto.run()

    return f"Heures ouvert, fermé: {hour_on_off}"

@pyaccess.route("/get_state_hour")
def get_state_hour():
    """
    RETURN: { "on" : <int>
              "off": <int> }
    """
    return {"on": hour_on_off[0], "off": hour_on_off[1]}
