from flask import Flask, escape, request, render_template, Response
from flask import Blueprint
from datetime import datetime

from PyWubook.main import get_price

billboardprice = Blueprint("billboardprice", __name__, url_prefix="/price", template_folder='templates', static_folder='static')

@billboardprice.route("/help")
def help():
    return ""

@billboardprice.route("/")
def index():
    return render_template("billboard_price/index.html")

@billboardprice.route("/room/<room>")
def price(room):
    # TODO: gerer l’erreur potentiel et mettre un prix par défaut.
    try:
        resp = get_price(room)
    except Exception as e:
        resp = "Demander à la reception"

    resp = Response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp