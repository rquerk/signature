import socket
import sys
import rsa
import client_lib as service
from rsa.pkcs1 import VerificationError

host = "localhost"

def new_socket(port):
    soc = service.socket_create()
    remote_ip = socket.gethostbyname(host)
    soc.connect((remote_ip, port))
    return soc

def read_input():
    return str(sys.argv[1])
    
def send_input_to_server(soc):
    request = read_input()
    service.send_bytes_to_socket(soc, request.encode())
    service.send_bytes_to_socket(soc, service.close_bytes)

def receive_response(soc):
    return service.receive_bytes_from_socket(soc)

def close_socket(soc):
    soc.shutdown(socket.SHUT_RDWR)
    soc.close()

def test_receives_a_key():
    publish_port = 5422
    soc = new_socket(publish_port)
    key = receive_response(soc)
    return key

def test_same_input_results_to_same_output():
    signer_port = 5421
    soc = new_socket(signer_port)
    send_input_to_server(soc)
    response = receive_response(soc)
    close_socket(soc)
    
    soc2 = new_socket(signer_port)
    send_input_to_server(soc2)
    response2 = receive_response(soc2)
    close_socket(soc2)
    
    if response != response2:
        print("ERROR: Not The Same Server Output by same Input")
        exit(-1)
    
    return response
   
if __name__ == "__main__":
    
    signature = test_same_input_results_to_same_output()
    key = test_receives_a_key()
    rsa_key = rsa.PublicKey.load_pkcs1(key)
    try:
        hash_type = rsa.verify(sys.argv[1].encode(), signature, rsa_key)
        print("verification succeeded; hash type used: ", hash_type)
    except VerificationError:
        print("verification failed")
        exit(-1)
