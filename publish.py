from socketserver import StreamRequestHandler
from socketserver import TCPServer


class MyTCPHandler(StreamRequestHandler):

    def handle(self):
        with open(r"/home/levi/public_key_file", "br") as pub_key_file:
            content = pub_key_file.read()
        # self.wfile is a file-like object used to write to the client
        self.wfile.write(content)
        
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 9998
    
    try:
        with TCPServer((HOST, PORT), MyTCPHandler) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        exit(0)
