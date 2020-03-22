import sys, os
import logging
C = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(filename=os.path.join(C, "run_server.log"), level=logging.DEBUG, format="%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

pyaccess_abs_path = os.path.join(C, "PyAccess")
pywubook_abs_path = os.path.join(C, "PyWubook")
sys.path.append(pyaccess_abs_path)
sys.path.append(pywubook_abs_path)
from server.views import app

app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)