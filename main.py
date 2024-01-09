# from flask_socketio import SocketIO
from website import create_app

app = create_app()
# socketio = SocketIO(app)

if __name__ == '__main__':
    app.run(debug=True)

