# from flask import Blueprint
# import schedule

# pyaccess = Blueprint("pyaccess", __name__, url_prefix="/pyaccess")

from .views import pyaccess

# from PyAccess import lock_door

# pin_door = 5  # channel 1  serrure porte d’entrée
# pin_2 = 6  # ch2  lumières enseignes
# pin_3 = 13  # ch3  lumières out-réceptions
# pin_4 = 16  # ch4  lumières paliers
# pin_5 = 19  # ch5  lumières salle petit-dej
# pin_6 = 20  # ch6  lumières banque
# pin_7 = 21  # ch7  lumieres in-reception
# pin_8 = 26  # ch8