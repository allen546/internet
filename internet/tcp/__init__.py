from socket import *
import ssl
class TCPServer:
    def __init__(self, addr, handler, ssl=False, ssl_cert=None, cafile=None, threaded=False, workers=1):
        self._socket = socket()
        self.ssl = ssl
        self.addr = addr
        self.handler = handler()
        self._socket.bind(addr)
        self.history = []
        self.threaded = threaded
        if ssl:
            context = SSLContext(ssl_protocol, cafile)
            context.load_default_certs(purpose=Purpose.SERVER_AUTH)
            context.load_cert_chains(ssl_cert)
            self._socket = context.wrap_socket(self._socket, server_side=True, do_handshake_on_connect=True, suppress_ragged_eofs=True, server_hostname=None, session=None)
        self._handler = handler()
        self.workers = workers
    def _run(self):
        self._socket.listen()
        while True:
            conn, addr = self._socket.accept()
            self.history.append('ACCEPT ' + str(addr))
            while True:
                data = conn.recv(65535)
                self.history.append('RECV ' + repr(data))
                data, exit_true = self._handler.handle(data)
                self.history.append('HANDLE_OUTPUT ' + data + str(exit_true))
                if exit_true == True:
                    conn.close()
                    self.history.append('CLOSE ' + repr(conn))
                    break
                conn.sendall(data)
                self.history.append('SEND ' + repr(data))
    def run(self):
        if self.threaded:
            self.threads = []
            import threading
            try:
                for i in range(self.workers):
                    thread = threading.Thread(target=self._run, daemon=True)
                    self.threads.append(thread)
                    thread.start()
            except:
                raise SystemExit
        else:
            self._run()
