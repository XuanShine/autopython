# from flask import Blueprint
import schedule

# pyaccess = Blueprint("pyaccess", __name__, url_prefix="/pyaccess")

from .views import pyaccess

from PyAccess import lock_door

# pin_door = 5  # channel 1  serrure porte d’entrée
# pin_2 = 6  # ch2  lumières enseignes
# pin_3 = 13  # ch3  lumières out-réceptions
# pin_4 = 16  # ch4  lumières paliers
# pin_5 = 19  # ch5  lumières salle petit-dej
# pin_6 = 20  # ch6  lumières banque
# pin_7 = 21  # ch7  lumieres in-reception
# pin_8 = 26  # ch8

# porte
schedule.every().day.at(f"07:00").do(lock_door.open_door).tag("open_door")
schedule.every().day.at(f"22:00").do(lock_door.close_door).tag("close_door")
# lumière enseignes
schedule.every().day.at(f"06:00").do(lock_door.turn, "off", lock_door.pin_2).tag("off")
schedule.every().day.at(f"21:00").do(lock_door.turn, "on", lock_door.pin_2).tag("on")
# lumière banquet
schedule.every().day.at(f"22:00").do(lock_door.turn, "off", lock_door.pin_6).tag("off")
schedule.every().day.at(f"15:00").do(lock_door.turn, "on", lock_door.pin_6).tag("on")
# lumière out-reception
schedule.every().day.at(f"23:00").do(lock_door.turn, "off", lock_door.pin_3).tag("off")
schedule.every().day.at(f"07:00").do(lock_door.turn, "on", lock_door.pin_3).tag("on")
# lumière paliers
schedule.every().day.at(f"08:00").do(lock_door.turn, "off", lock_door.pin_4).tag("off")
schedule.every().day.at(f"18:00").do(lock_door.turn, "on", lock_door.pin_4).tag("on")
# pin_7 = 21  # ch7  lumieres in-reception
schedule.every().day.at(f"12:00").do(lock_door.turn, "off", lock_door.pin_4).tag("off")
schedule.every().day.at(f"15:00").do(lock_door.turn, "on", lock_door.pin_4).tag("on")



task_auto = schedule.every().hour.do(lock_door.main, 7, 22).tag("auto_door")
task_auto.run()

