class Handler:
    def __init__(self):
        self.trace = []
    def handle(self, data):
        self.trace.append(f'HANDLE {data}')
        return data
