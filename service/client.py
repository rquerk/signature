import socket
import sys

from backup.kindaTrash import service


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

print(response, file=sys.stdout)
