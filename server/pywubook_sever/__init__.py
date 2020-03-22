from flask import Blueprint

pywubook = Blueprint("pywubook", __name__)

from . import views

import schedule
from PyWubook.main import main
schedule.every().day.do(main)