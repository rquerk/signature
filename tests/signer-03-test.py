#!/bin/python3

import client_lib


def test_receives_a_key():
    publish_port = 5422
    soc = client_lib.new_connected_socket(publish_port)
    pub_key = client_lib.receive_bytes_from_socket(soc)
    if len(pub_key) < 426:
        print("ERROR: Key returned by publish is too short")
        exit(3)
    if not pub_key[:30].decode(encoding="utf-8") == "-----BEGIN RSA PUBLIC KEY-----":
        print("key is not in PEM Format, head is missing")
        print(pub_key[:30])
        exit(3)
    if not pub_key[-29:-1].decode(encoding="utf-8") == "-----END RSA PUBLIC KEY-----":
        print("key is not in PEM Format, tail is missing")
        print(pub_key[-29:-1])  # in the end there is a newline \n
        exit(3)
    return


if __name__ == "__main__":
    test_receives_a_key()
    print("OK: Got a String not smaller 426 bytes with PEM markers from Port 5422")
    exit(1)
