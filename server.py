from flask import Flask, render_template
from threading import Thread
from flask import request
from flask_socketio import SocketIO, send, emit

app = Flask("")
socketio = SocketIO(app)
users = {}

@socketio.on('sendmsg')
def handle_message(data):
    print('received message: ' + str(data))
    print("test")
    emit("updatemsg", data, broadcast=True)


@socketio.on('onconnected')
def handle_message(data):
    print('received message: con ' + str(data))


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


@socketio.on('earn')
def handle_message(data):
    if data["user"] not in users:
        users[data["user"]] = 1
    else:
        user[data["user"]] += 1
    emit("updatepnt", {"pnt": users[data["user"]]})
    lb = dict(sorted(users.items(), key=lambda item: item[1]))
    emit("leaderboard", {"lb": str(lb).replace(",","\n")}, broadcast=True)

@app.route("/clicker", methods=["POST", "GET"])
def clicker():
    print("user connect to home")
    if request.method == "GET":
        print("get")
        return render_template("clicker.html")
    

    return "nothing to show"

def run_server():
    print("Im starting...")
    socketio.run(app, allow_unsafe_werkzeug=True, host="0.0.0.0", port=80, debug=True)
    print("Im online baby !")







run_server()


