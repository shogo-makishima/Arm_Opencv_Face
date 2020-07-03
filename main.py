from Classes.Main import Main
from Classes.Settings import Settings
from flask import Flask, render_template, request, jsonify
import os, asyncio, serial.tools.list_ports

main = Main()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/_get_image/", methods=["GET", "POST"])
def SendImage():
    return jsonify({"image": main.ImageToBase64(main.GetImage())})


@app.route("/_get_cascades/", methods=["GET", "POST"])
def SendCascades():
    cascades = list(filter(lambda x: x.endswith('.xml'), os.listdir("Files/")))
    return jsonify({"cascades": cascades})


@app.route("/_get_ports/", methods=["GET", "POST"])
def SendPorts():
    ports = [i.device for i in list(serial.tools.list_ports.comports())]
    return jsonify({"ports": ports})


@app.route("/_send_settings/", methods=["GET", "POST"])
def GetSettings():
    try:
        print(f'cascade: {request.form["cascade"]};\nport: {request.form["port"]};\nscaleFactor: {request.form["scaleFactor"]};\nminNeighbors: {request.form["minNeighbors"]};\narea: {request.form["area"]};\nkey: {request.form["key"]}')
        if (request.form["key"] != Settings.key): return jsonify({"response": 900})
        Settings.SetSetting(Settings, float(request.form["scaleFactor"]), int(request.form["minNeighbors"]), int(request.form["area"]), 0, request.form["cascade"], request.form["port"])
        asyncio.run(main.Start())
    except Exception as e:
        print(e)
        return jsonify({"response": 500})
    return jsonify({"response": 200})


if (__name__ == "__main__"): app.run(host="0.0.0.0", port=5000)

