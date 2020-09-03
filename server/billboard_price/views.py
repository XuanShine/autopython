from flask import Flask, escape, request, render_template, Response
from flask import Blueprint
from datetime import datetime

billboardprice = Blueprint("billboardprice", __name__, url_prefix="/price", template_folder='templates', static_folder='static')

@billboardprice.route("/help")
def help():
    return ""

@billboardprice.route("/")
def index():
    return render_template("billboard_price/index.html")

@billboardprice.route("/room/<room>")
def price(room):
    # TODO: GET_PRICE
    if room == "sstd":
        resp = "67"
    elif room == "sblc":
        resp = "74"
    elif room == "dstd":
        resp = "74"
    elif room == "dblc":
        resp = "82"
    elif room == "tstd":
        resp = "86"
    elif room == "tblc":
        resp = "94"
    elif room == "fblc":
        resp = "148"
    resp = Response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp