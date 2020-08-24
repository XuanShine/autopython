from . import create_app, initialize_extensions
from .models import RaspberryPi
import os
C = os.path.abspath(os.path.dirname(__file__))
import logging

app = create_app()
initialize_extensions(app)


@app.route("/help")
def help():
    return """/pyaccess/help"""

@app.route("/")
def hellotest():
    return "In view.py server"


@app.route("/logs")
def logs():
    result = ""
    for file in os.listdir():
        if file.endswith(".log"):
            with open(file, "r") as f_in:
                result += f"{file} :\n {f_in.read()}\n{'=' * 50}\n"
    for file in os.listdir(".."):
        if file.endswith(".log"):
            with open(os.path.join("..", file), "r") as f_in:
                result += f"{file} :\n {f_in.read()}\n{'=' * 50}\n"
    return result.replace("\n", "<br>")

@app.route("/id")
def id():
    """Self identity"""
    with open(os.path.join("..", "RPI_ID"), "r") as f_in:
        RPI_ID = f_in.read().strip()
    return RPI_ID


# @app.route("/register_ip/<ip>/<id>")
# def register_ip(ip, id):
#     """ For the main RPI: register others RPI identity and ip"""
#     rpi = RaspberryPi.query.get(name=id)
#     if rpi and rpi.ip_address == ip:
#         return ""
#     if not rpi:
#         logging.info(f"New register: {id} : {ip}")
#     elif rpi.ip_address != ip:
#         logging.info(f"IP changed: {id} : {rpi.ip_address} -> {ip}")
#         db.session.delete(rpi)
#     new = RaspberryPi(name=id, ip_address=ip)
#     db.session.add(new)
#     db.session.commit()
#     return ""