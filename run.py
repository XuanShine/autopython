import sys, os
from server.views import app


C = os.path.abspath(os.path.dirname(__file__))

pyaccess_abs_path = os.path.join(C, "PyAccess")

sys.path.append(pyaccess_abs_path)

app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)