from flask import Flask, render_template
from threading import Thread
from flask import request

app = Flask("")

@app.route("/", methods=["POST", "GET"])
def home():
    print("user connect to home")
    if request.method == "POST":
        data = request.form
        print(data)
        print("post")
        return "send !"

    if request.method == "GET":
        print("get")
        render_template("index.html")
        return "coucou toi!"

    return "nothing to show"

def run_server():
    print("Im starting...")
    app.run(host='0.0.0.0', port=8080)
    print("Im online baby !")
run_server()
