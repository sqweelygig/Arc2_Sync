from bin.Factory import FactoryReadOnly


class SimsBase(FactoryReadOnly):
    def __init__(self, connection, item_settings):
        try:
            super().__init__(connection, item_settings)
        except NotImplementedError:
            pass

    def get(self):
        items = self.list()
        output = []
        for item in items:
            value = self.map(item)
            if value is not None:
                output.append(value)
        return output

    def list(self):
        raise NotImplementedError

    @staticmethod
    def map(item):
        return item
