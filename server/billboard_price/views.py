from flask import Flask, escape, request, render_template, Response, jsonify
from flask import Blueprint
from datetime import datetime

from PyWubook.main import get_prices_avail_today, room_to_code

billboardprice = Blueprint("billboardprice", __name__, url_prefix="/price", template_folder='templates', static_folder='static')

@billboardprice.route("/help")
def help():
    return ""

@billboardprice.route("/")
def index():
    return render_template("billboard_price/index.html")

@billboardprice.route("/room/<room>")
def price(room):
    try:
        prices, avails = get_prices_avail_today()
        # prices : {<roomcode>: [price, ...], ...}
    except Exception as e:
        resp = "Demander à la reception"
    if room == "all":
        code_to_room = { room_to_code[room]: room for room in room_to_code.keys() }
        resp = dict()
        for code_room in prices.keys():
            if code_room in code_to_room:
                if avails[code_room][0]["closed"] == 1:
                    resp[code_to_room[code_room]] = "COMPLET"
                elif code_room == "405127":  # single eco
                    if avails["329039"][0]["avail"] == 0:
                        resp[code_to_room[code_room]] = "COMPLET"
                    else:
                        resp[code_to_room[code_room]] = round(prices[code_room][0])
                elif  code_room == "405126":  # single balcon
                    if avails["329667"][0]["avail"] == 0:
                        resp[code_to_room[code_room]] = "COMPLET"
                    else:
                        resp[code_to_room[code_room]] = round(prices[code_room][0])
                else:
                    if avails[code_room][0].get("avail") > 0:
                        resp[code_to_room[code_room]] = round(prices[code_room][0])
                    elif avails[code_room][0].get("avail") == 0:
                        resp[code_to_room[code_room]] = "COMPLET"
                    else:
                        resp[code_to_room[code_room]] = "Erreur"

        resp = jsonify(resp)
    else:
        resp = round(prices[room_to_code[room]][0])
        resp = Response(resp)


    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

# TODO: afficher "COMPLET" quand il n’y a plus de chambre.