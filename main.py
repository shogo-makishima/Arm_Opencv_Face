from Classes.Main import Main
from Classes.Settings import Settings
from flask import Flask, render_template, request, jsonify
import os

main = Main()
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/_get_image/", methods=["GET", "POST"])
def SendImage() -> str:
    return jsonify({"image": main.ImageToBase64(main.GetImage())})


@app.route("/_get_cascades/", methods=["GET", "POST"])
def SendCascades() -> str:
    cascades = list(filter(lambda x: x.endswith('.xml'), os.listdir("Files\\")))
    return jsonify({"cascades": cascades})


@app.route("/_send_settings/", methods=["GET", "POST"])
def GetSettings() -> str:
    try:
        print(f'cascade: {request.form["cascade"]};\nscaleFactor: {request.form["scaleFactor"]};\nminNeighbors: {request.form["minNeighbors"]};\narea: {request.form["area"]};\nkey: {request.form["key"]}')
        if (request.form["key"] != Settings.key): return jsonify({"response": 900})
        Settings.SetSetting(Settings, float(request.form["scaleFactor"]), int(request.form["minNeighbors"]), int(request.form["area"]), 0, request.form["cascade"])
        main.Start()
    except: return jsonify({"response": 500})
    return jsonify({"response": 200})


if (__name__ == "__main__"): app.run(host="0.0.0.0", port=5000)

