from flask import Flask, escape, request
from . import pywubook

from PyWubook import main

@pywubook.route("/update")
@pywubook.route("/update/<int:days>")
def update(days=360):
    try:
        main.main(days)
    except Exception:
        import traceback
        logging.error(f"Exception dans la fonction update_price_wubook, ce job est arrêté: \n{traceback.format_exc()}")
    return "Done"