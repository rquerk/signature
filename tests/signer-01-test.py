#!/bin/python3

import client_lib


def test_receives_answer_after_input():
    signer_port = 5421
    soc = client_lib.new_connected_socket(signer_port)
    client_lib.send_input_to_server(soc)
    response = client_lib.receive_bytes_from_socket(soc)
    client_lib.close_socket(soc)

    return response


if __name__ == "__main__":

    answer = None
    try:
        answer = test_receives_answer_after_input()
    except RuntimeError as re:
        print("Test 01 - Get Answer from Signer - Failed")
        print(re)
        exit(3)

    if answer:
        print("OK: Got Answer from Signer")
        print(answer.hex()[:10] + "...")
        exit(1)

    print("No Error during test, but got no answer from Signer!")
    exit(2)
