import unittest
import service
import establish_connection


class ServerTestClass(unittest.TestCase):

    def test_server_accepts_client_connection(self):
        server = EstablishConnection.socket_create_bind_and_listen()
        client = EstablishConnection.socket_create_and_connect()

    # def test_send_bytes_to_socket(self):
    #    self.assertEqual(send_bytes_to_socket(test_socket, b"A"), 1)


if __name__ == '__main__':
    unittest.main()
