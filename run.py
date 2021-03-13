import sys, os
import logging
C = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(filename=os.path.join(C, "run_server.log"), level=logging.DEBUG, format="%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

from server.views import app

try:
    with open(os.path.join(C, "..", "RPI_ID"), "r") as f_in:
        RPI_ID = f_in.read().strip()
except FileNotFoundError:
    RPI_ID = "undefined"

# TODO: télécharger les fichiers nécessaires.

if RPI_ID == "entry":
    pyaccess_abs_path = os.path.join(C, "PyAccess")
    sys.path.append(pyaccess_abs_path)
    from server.pyaccess_server import pyaccess
    app.register_blueprint(pyaccess, url_prefix="/pyaccess")

    pywubook_abs_path = os.path.join(C, "PyWubook")
    sys.path.append(pywubook_abs_path)
    from server.pywubook_server import pywubook
    app.register_blueprint(pywubook, url_prefix="/pywubook")

    from server.billboard_price.views import billboardprice
    app.register_blueprint(billboardprice, url_prefix="/price")

elif RPI_ID == "ring":
    pydoorbird_abs_path = os.path.join(C, "PyDoorbird")
    sys.path.append(pydoorbird_abs_path)
    from server.pydoorbird_server import pydoorbird
    app.register_blueprint(pydoorbird)


# app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)


from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher

d = PathInfoDispatcher({'/': app})
server = WSGIServer(('0.0.0.0', 5000), d)

if __name__ == '__main__':
   try:
      server.start()
   except KeyboardInterrupt:
      server.stop()