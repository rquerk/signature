from server import Server

from lib.client_list import ClientList
from lib.establish_connection import ServerSocketConnection
from lib.send.sending import Transmitter
from lib.service import Service

from time import sleep

if __name__ == "__main__":
    try:

        server_socket = ServerSocketConnection()
        clients = ClientList()
        server = Server(server_socket, clients)
        server.start()

        while True:
            client_wrap = server.new_client()
            transmitter = Transmitter()
            signature = Service(client_wrap, transmitter)
            server.process_client(signature)
            sleep(1)  # prevents the server from taking all the cpu resources

    except KeyboardInterrupt:
        exit(0)
