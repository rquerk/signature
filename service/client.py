import socket
import sys

import client_lib as service


host = "localhost"
port = 5421

soc = service.socket_create()
remote_ip = socket.gethostbyname(host)
soc.connect((remote_ip, port))

request = input()
service.send_bytes_to_socket(soc, request.encode(service.encoding_type))
service.send_bytes_to_socket(soc, service.close_bytes)

response = service.receive_bytes_from_socket(soc)

soc.shutdown(socket.SHUT_RDWR)
soc.close()

print(fr"{response}", file=sys.stdout)
# .decode("utf_8", errors="ignore")
