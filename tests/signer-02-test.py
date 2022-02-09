#!/bin/python3

import client_lib


def test_same_input_results_to_same_output():
    signer_port = 5421
    soc = client_lib.new_connected_socket(signer_port)
    client_lib.send_input_to_server(soc)
    response = client_lib.receive_bytes_from_socket(soc)
    client_lib.close_socket(soc)

    soc2 = client_lib.new_connected_socket(signer_port)
    client_lib.send_input_to_server(soc2)
    response2 = client_lib.receive_bytes_from_socket(soc2)
    client_lib.close_socket(soc2)

    if response != response2:
        print("ERROR - SIGNER SERVICE: Server responds with different answers for same input")
        exit(3)

    return


if __name__ == "__main__":
    test_same_input_results_to_same_output()
    print("OK: Same input  to signer results in same output")
    exit(1)
