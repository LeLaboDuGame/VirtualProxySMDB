from flask import Flask, render_template
from threading import Thread
from flask import request
from flask_socketio import SocketIO, send, emit
import json

app = Flask("")
socketio = SocketIO(app)
users = {}
path="./save.json"
r=0

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
    global r
    if data["user"] not in users:
        users[data["user"]] = [1,1]
    else:
        users[data["user"]][0] += users[data["user"]][1]
    emit("updatepnt", {"pnt": users[data["user"]][0]})
    pdict = {}
    for k in users.keys():
        pdict[k] = users[k][0]
    lb = dict(sorted(pdict.items(), key=lambda item: item[1]))
    lb = {v: k for k, v in lb.items()}
    emit("leaderboard", {"lb": str(lb)}, broadcast=True)
    r+=1
    if r == 10:
        r=0
        file = open(path, "w")
        file.write(json.dumps(users))
        file.close()
        print("saved !")


@socketio.on('buy')
def handle_message(data):
    if data["user"] not in users:
        users[data["user"]] = [1,1]
    u = users[data["user"]]
    if u[0] >= 2**u[1] :
        u[0] -= 2** u[1]
        u[1] += 1
    users[data["user"]] = u
    emit("updateearn", {"mul": users[data["user"]][1]})
    emit("updatepnt", {"pnt": users[data["user"]][0]})
        


@app.route("/clicker", methods=["POST", "GET"])
def clicker():
    print("user connect to home")
    if request.method == "GET":
        print("get")
        return render_template("clicker.html")
    

    return "nothing to show"

def run_server():
    users = json.load(open(path, "r"))
    print("Im starting...")
    socketio.run(app, allow_unsafe_werkzeug=True, host="0.0.0.0", port=80, debug=True)
    print("Im online baby !")







run_server()


