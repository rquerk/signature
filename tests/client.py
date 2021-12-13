import socket
import sys

import client_lib as service


host = "localhost"
port = 5421


def new_socket():
    soc = service.socket_create()
    remote_ip = socket.gethostbyname(host)
    soc.connect((remote_ip, port))
    return soc

def read_input():
    return str(sys.argv[1])
    
def send_input_to_server(soc):
    request = read_input()
    service.send_bytes_to_socket(soc, request.encode(service.encoding_type))
    service.send_bytes_to_socket(soc, service.close_bytes)

def receive_response(soc):
    return service.receive_bytes_from_socket(soc)

def close_socket(soc):
    soc.shutdown(socket.SHUT_RDWR)
    soc.close()
    
if __name__ == "__main__":
    
    soc = new_socket()
    send_input_to_server(soc)
    response = receive_response(soc)
    close_socket(soc)
    
    soc2 = new_socket()
    send_input_to_server(soc2)
    response2 = receive_response(soc2)
    close_socket(soc2)
    
    if response != response2:
        exit(-1)
        
    print(fr"{response, response2}", file=sys.stdout)
    # .decode("utf_8", errors="ignore")
