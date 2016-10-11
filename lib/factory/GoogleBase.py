from bin.Factory import Factory


class GoogleBase(Factory):
    def get(self):
        items = self.list()
        output = []
        for item in items:
            value = self.map(item)
            if value is not None:
                output.append(value)
        return output

    def __init__(self, connection, settings):
        super().__init__(connection, settings)

    def list(self):
        raise NotImplementedError

    def map(self, item):
        return item
