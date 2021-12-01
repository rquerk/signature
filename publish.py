import socketserver

class MyTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        with open("/home/levi/public_key_file", "r") as pub_key_file:
            content = pub_key_file.read().encode()
        # self.wfile is a file-like object used to write to the client
        self.wfile.write(content)
        
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 9998
    
    try:
        with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        exit(0)
