import sys, os
import logging
C = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(filename=os.path.join(C, "run_server.log"), level=logging.DEBUG, format="%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

from server.views import app

with open(os.path.join("..", "RPI_ID"), "r") as f_in:
    RPI_ID = f_in.read().strip()

if RPI_ID == "entry":
    pyaccess_abs_path = os.path.join(C, "PyAccess")
    pywubook_abs_path = os.path.join(C, "PyWubook")
    sys.path.append(pyaccess_abs_path)
    sys.path.append(pywubook_abs_path)

    from server.pyaccess_server import pyaccess
    from server.pywubook_sever import pywubook
    app.register_blueprint(pyaccess)
    app.register_blueprint(pywubook)
elif RPI_ID == "ring":
    pydoorbird_abs_path = os.path.join(C, "PyDoorbird")
    sys.path.append(pydoorbird_abs_path)
    from server.pydoorbird_server import pydoorbird
    app.register_blueprint(pydoorbird)

app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)