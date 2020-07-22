import os
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = "mysecret1234"
socketio = SocketIO(app)

user_no = 1

@app.before_request
def before_request():
    global user_no
    if 'session' in session and 'user-id' in session:
        pass
    else:
        session['session'] = os.urandom(24)
        session['username'] = 'user'+str(user_no)
        user_no += 1

@app.route("/" , methods=['GET'])
def home():
    return render_template("chat.html")

@socketio.on('connect')
def connect():
    emit("receiveChat", {'data': 'connected', 'username': session['username']})

@socketio.on('disconnect')
def disconnect():
    session.clear()

@socketio.on("sendChat")
def request(message):
    emit("receiveChat", {'data': message['data'], 'username': session['username']}, broadcast=True) 

if __name__ == '__main__':
    socketio.run(app)