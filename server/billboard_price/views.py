from flask import Flask, escape, request, render_template, Response, jsonify
from flask import Blueprint
from datetime import datetime

from PyWubook.main import get_prices_today, room_to_code

billboardprice = Blueprint("billboardprice", __name__, url_prefix="/price", template_folder='templates', static_folder='static')

@billboardprice.route("/help")
def help():
    return ""

@billboardprice.route("/")
def index():
    return render_template("billboard_price/index.html")

@billboardprice.route("/room/<room>")
def price(room):
    # TODO: gerer l’erreur potentielle et mettre un prix par défaut.
    # TODO: chercher aussi les disponibilités pour afficher "COMPLET"
    try:
        prices = get_prices_today()
        # prices : {<roomcode>: [price, ...], ...}
    except Exception as e:
        resp = "Demander à la reception"
    if room == "all":
        code_to_room = { room_to_code[room]: room for room in room_to_code.keys() }
        resp = {code_to_room[room]: round(prices[room][0]) for room in prices.keys() if room in code_to_room}
        resp = jsonify(resp)
    else:
        resp = round(prices[room_to_code[room]][0])
        resp = Response(resp)


    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp