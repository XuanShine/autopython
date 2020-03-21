from . import app

@app.route("/hellotest")
def hellotest():
    return "In  view.py server"