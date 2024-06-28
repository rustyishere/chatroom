from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'alkdnfencakenan'
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat/<room_id>')
def chat(room_id):
    return render_template('chat.html', room_id=room_id)


@socketio.on('join')
def handle_join(data):
    username = data['username']
    room_id = data['room_id']
    join_room(room_id)
    message = f'{username} has joined the room.'
    send({'message': message}, room=room_id)
    print(message)  


@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room_id = data['room_id']
    leave_room(room_id)
    send(f'{username} has left the room.', room=room_id)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    room_id = data['room_id']
    message = data['message']
    send({'username': username, 'message': message}, room=room_id)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)