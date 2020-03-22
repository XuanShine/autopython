from . import app
import os
C = os.path.abspath(os.path.dirname(__file__))

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
