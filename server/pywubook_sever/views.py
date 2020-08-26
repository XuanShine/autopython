from flask import Flask, escape, request
from . import pywubook
import logging

from PyWubook import main

@pywubook.route("/help")
def help():
    return "/update or /update/<int:days>"

@pywubook.route("/update")
@pywubook.route("/update/<int:days>")
def update(days=360):
    try:
        main.main(days)
    except Exception:
        import traceback
        logging.error(f"Exception dans la fonction update_price_wubook: \n{traceback.format_exc()}")
    return "Done"