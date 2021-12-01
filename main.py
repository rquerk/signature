from service.server import Server

from service.lib.client_list import ClientList
from service.lib.establish_connection import ServerSocketConnection
from service.lib.send.sending import Transmitter
from service.lib.service import Service

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
