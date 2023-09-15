import config
from threading import Thread
from client.app import app as client_app
from server.app import app as server_app
from db.app import app as db_app

server_host = "0.0.0.0"

def db_run():
    db_app.run(host=server_host, port=config.DB_PORT)

def server_run():
    server_app.run(host=server_host, port=config.SERVER_PORT)

def client_run():
    client_app.run(host="localhost", port=config.CLIENT_PORT)

Thread(target=db_run).start()
Thread(target=server_run).start()
Thread(target=client_run).start()
