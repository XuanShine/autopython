# from flask import Blueprint
import schedule

# pyaccess = Blueprint("pyaccess", __name__, url_prefix="/pyaccess")

from .views import pyaccess

from PyAccess import lock_door

# pin_door = 5  # channel 1  serrure porte d’entrée
# pin_2 = 6  # ch2  lumières enseignes
# pin_3 = 13  # ch3  lumières out-réceptions
# pin_4 = 16  # ch4  lumières paliers
# pin_5 = 19  # ch5  lumieres in-reception
# pin_6 = 20  # ch6  lumières banque
# pin_7 = 21  # ch7  lumières salle petit-dej buffet
# pin_8 = 26  # ch8  lumières salle petit-dej tables

# init all
init_GPIO = schedule.every().hour.do(lock_door.init_GPIO).tag("init")
init_GPIO.run()
init_lamp = schedule.every().hour.do(lock_door.init_lamp).tag("init")
init_lamp.run()
schedule.clear("init")


# check lock every hour
task_auto = schedule.every().hour.do(lock_door.main, 7, 22).tag("auto_door")
task_auto.run()
# check light every night
task_light = schedule.every().day.at("23:00").do(lock_door.init_lamp)

# porte
schedule.every().day.at(f"07:00").do(lock_door.open_door).tag("open_door")
schedule.every().day.at(f"22:00").do(lock_door.close_door).tag("close_door")
# lumière enseignes
schedule.every().day.at(f"06:00").do(lock_door.turn, "off", 2).tag("off")
schedule.every().day.at(f"19:00").do(lock_door.turn, "on", 2).tag("on")
# lumière banque
schedule.every().day.at(f"22:00").do(lock_door.turn, "off", 6).tag("off")
schedule.every().day.at(f"15:00").do(lock_door.turn, "on", 6).tag("on")
# lumière out-reception
schedule.every().day.at(f"23:00").do(lock_door.turn, "off", 3).tag("off")
schedule.every().day.at(f"07:00").do(lock_door.turn, "on", 3).tag("on")
# lumière paliers
schedule.every().day.at(f"08:00").do(lock_door.turn, "off", 4).tag("off")
schedule.every().day.at(f"18:00").do(lock_door.turn, "on", 4).tag("on")
# ch5  lumieres in-reception
schedule.every().day.at(f"12:00").do(lock_door.turn, "off", 5).tag("off")
schedule.every().day.at(f"15:00").do(lock_door.turn, "on", 5).tag("on")
# ch7 lumiere petit-dej buffet
schedule.every().day.at(f"06:00").do(lock_door.turn, "on", 7).tag("on")
schedule.every().day.at(f"23:00").do(lock_door.turn, "off", 7).tag("off")
# ch8 lumiere petit-dej tables
schedule.every().day.at(f"07:30").do(lock_door.turn, "on", 8).tag("on")
schedule.every().day.at(f"11:00").do(lock_door.turn, "off", 5).tag("off")
