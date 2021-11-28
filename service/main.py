from lib.service import Service
from lib.send.sending import Transmitter
from server import Server
from time import sleep

if __name__ == "__main__":
    try:
        server = Server()
        server.start()

        while True:
            client_wrap = server.new_client()
            transmitter = Transmitter()
            signature = Service(client_wrap, transmitter)
            server.process_client(signature)
            sleep(1)  # prevents the server from taking all the cpu resources

    except KeyboardInterrupt:
        exit(0)
        