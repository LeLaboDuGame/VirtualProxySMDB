from flask import Flask, render_template
from threading import Thread
from flask import request
from flask_socketio import SocketIO

app = Flask("")
socketio = SocketIO(app)

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
        return render_template("index.html")
    

    return "nothing to show"



def run_server():
    print("Im starting...")
    socketio.run(app, allow_unsafe_werkzeug=True)
    print("Im online baby !")






@socketio.on('sendmsg')
def handle_message(data):
    print('received message: ' + data)


@socketio.on('onconnected')
def handle_message(data):
    print('received message: con ' + data)

run_server()


