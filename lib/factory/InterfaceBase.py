from bin.Factory import Factory


class InterfaceBase(Factory):
    def __init__(self, connection, settings):
        try:
            super().__init__(connection, settings)
        except NotImplementedError:
            pass

    def fetch(self):
        return []

    def put(self, item):
        pass

    def map(self, item):
        return item

    def delete(self, item):
        pass

    def patch(self, item):
        pass
