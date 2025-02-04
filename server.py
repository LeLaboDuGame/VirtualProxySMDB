from flask import Flask
from threading import Thread
from flask import request

app = Flask("")

@app.route("/", methods=["POST"])
def home():
    print("user connect to home")
    if request.method == "POST":
        data = request.form
        print(data)
        print("post")

    if request.method == "GET":
        print("get")

    return "Le plus beau des bot est en ligne ! genre vrmt le plus beau ! Regarde comment je suis beau et fort ! JE PING ET OUI JE PING DANS UN CHANNEL TRUC DE DINGUE !!!!!!!!"

def run_server():
    print("Im starting...")
    app.run(host='0.0.0.0', port=8080)
    print("Im online baby !")
run_server()
