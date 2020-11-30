import os
from server.pywubook_server.views import update
C = os.path.abspath(os.path.dirname(__file__))

from flask import Blueprint

# pywubook = Blueprint("pywubook", __name__, url_prefix="/pywubook")

from .views import pywubook

import schedule, git, sys, logging
from importlib import reload
from git.exc import GitCommandError
from datetime import datetime, timedelta
from PyWubook.HotelRates import scrape


def update_price_wubook():
    wubook_abs_path = os.path.join(C, "..", "..", "PyWubook")
    g = git.cmd.Git(wubook_abs_path)
    sys.path.append(wubook_abs_path)
    from PyWubook import main as main_pywubook
    
    def wrapper(days):
        logging.info("Fonction update_price_wubook en cours d’exécution")
        
        try:
            pull_result = g.pull()
            if pull_result != 'Already up to date.':
                [reload(module) for module in list(sys.modules.values())[::-1] if "PyWubook" in str(module)]
                logging.info("Changed in PyWubook code. PyWubook’s modules reloaded.")

        except GitCommandError as e:
            logging.warning(f"Git not accessible, the function continue: {e}")
        
        
        try:
            main_pywubook.main(days)
        except Exception:
            # Annuler la plannification du job
            # if "update_price_wubook" in jobs:
            # 	schedule.cancel_job(jobs.get("update_price_wubook"))
            import traceback
            logging.error(f"Exception dans la fonction update_price_wubook, ce job est arrêté: \n{traceback.format_exc()}")
        logging.info("Fonction update_price_wubook FIN d’exécution")
    
    return wrapper


def update_price_first_time_of_the_day():
    scrape.main(31*4)
    update_price_wubook()(30*4)

schedule.every().day.at("01:00").do(update_price_first_time_of_the_day)
# schedule.every().day.at("01:00").do(scrape.main, 31*4)
# schedule.every().day.at("02:00").do(update_price_wubook(), 30*4)

schedule.every(30).minutes.do(scrape.main, 7)
schedule.every(30).minutes.do(update_price_wubook(), 7)