from socketserver import StreamRequestHandler
from socketserver import TCPServer
import os 

class MyTCPHandler(StreamRequestHandler):
    
    def handle(self):
        with open(fr"{os.environ['PUBLIC_KEY']}", "br") as pub_key_file:
            content = pub_key_file.read()
        self.wfile.write(content)
        
        
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 5422
    
    try:
        with TCPServer((HOST, PORT), MyTCPHandler) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        exit(0)
