import client_lib
import socket
import sys


def send_input_to_server(sock):
    request = read_input()
    client_lib.send_bytes_to_socket(sock, request.encode())
    client_lib.send_bytes_to_socket(sock, client_lib.close_bytes)


def read_input():
    user_input = input("To Sign: ")
    return user_input


def receive_response(sock):
    return client_lib.receive_bytes_from_socket(sock)


def close_socket(sock):
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()


if __name__ == "__main__":

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Usage:")
            print("signing: client.py 5421")
            print("get the public Key: client.py")
            exit(3)
    else:
        port = 5422

    soc = client_lib.new_connected_socket(port)

    if len(sys.argv) > 1:
        send_input_to_server(soc)
        print(receive_response(soc).hex())
    else:
        print(receive_response(soc).decode(encoding="utf-8", errors="replace")[:-1])  # -1 to take away trailing \n

    exit(1)
