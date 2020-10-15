from xmlrpc.server import SimpleXMLRPCServer
class XMLRPCServer:
    def __init__(self, addr):
        self._server = SimpleXMLRPCServer(addr)
    def register_function(self, function):
        self._server.register_function(function)
    def register_class_instant(self, class_instant):
        self._server.register_instant(class_instant, allow_dotted_names=True)
    def _prepare(self):
        self._server.register_multicall_functions()
    def run(self):
        try:
            self._server.serve_forever()
        except Exception:
            if __debug__:
                raise
        except KeyboardInterrupt:
            raise
        finally:
            raise SystemExit
