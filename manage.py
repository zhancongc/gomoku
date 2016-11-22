from flask import Manager, Server

manager=Manager(app)
server=Server(host='0.0.0.0',port=5000)
manager.add_command('runserver',server)

if __name__ == '__main__':
	manager.run()