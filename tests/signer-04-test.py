#!/bin/python3

import traceback
import rsa
from rsa.pkcs1 import VerificationError
import client_lib


def receive_key():
    publish_port = 5422
    soc = client_lib.new_connected_socket(publish_port)
    pub_key = client_lib.receive_bytes_from_socket(soc)

    return pub_key


def get_signature():
    signer_port = 5421
    soc = client_lib.new_connected_socket(signer_port)
    client_lib.send_input_to_server(soc)
    response = client_lib.receive_bytes_from_socket(soc)
    client_lib.close_socket(soc)
    
    return response


if __name__ == "__main__":
    
    try:
        signature = get_signature()
        key = receive_key()
        rsa_key = rsa.PublicKey.load_pkcs1(key)
        
        try:
            hash_type = rsa.verify(client_lib.read_input().encode(encoding="utf-8"), signature, rsa_key)
            print("OK: Verification succeeded; hash type used: ", hash_type)
            exit(1)
        except VerificationError:
            print("ERROR: Verification failed. RSAs verify function exits with 'VerificationError'")
            exit(3)
    except RuntimeError:
        print("RuntimeError during Test")
        traceback.print_exc()  # file=sys.stdout
        exit(3)
