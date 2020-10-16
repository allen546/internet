import socket
class UDPServer:
    class Error: pass
    def __init__(self, addr, handler, addr_family=socket.AF_INET):
        self._socket = socket.socket(addr_family, socket.SOCK_DGRAM)
        self.addr = addr
        self._socket.bind(addr)
        self._handler = handler()
        self.history = []
    def _run(self):
        while True:
            data, addr = self._socket.recvfrom(65535)
            self.history.append(f'RECV {data} FROM {addr}')
            data, exit = self._handler.handle(data)
            exit = str(exit)
            self.history.append(f'HANDLE {data} {exit}')
            if eval(exit):
                break
            self._socket.sendto(data, addr)
            self.history.append(f'SEND {data} TO {addr}')
    def run(self):
        try:
            self._run()
        except Exception as e:
            raise self.Error(e) from None
            
