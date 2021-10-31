class Payload():
    def __init__(self, message, data, code=0):
        self.error = code
        self.message = message
        _data = data if data else {}
        self.data = _data

    def toJSON(self):
        return self.__dict__