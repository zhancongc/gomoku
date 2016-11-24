from flask_script import Manager, Server
from app.chess import chess
from app.gomoku import *


manager=Manager(app)
server=Server(host='0.0.0.0',port=5000)
manager.add_command('runserver',server)


@manager.command
def run():
	socketio.run(flask.current_app, use_reloader=False)


if __name__ == '__main__':
	manager.run()
