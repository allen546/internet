from server.tcp import *
class MyHandler:
    def handle(self, data):
        if data != b'exit':
            return data, False
        return '', True
server=TCPServer(('192.168.1.117',8000), MyHandler)
server.run()
