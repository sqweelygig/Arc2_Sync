from bin.Factory import FactoryReadOnly


class SimsBase(FactoryReadOnly):
    def __init__(self, connection, item_settings):
        try:
            super().__init__(connection, item_settings)
        except NotImplementedError:
            pass
        self.items = None

    def get(self, find=None):
        if self.items is None:
            self.items = self.list()
        if find is None:
            output = []
            for item in self.items:
                value = self.map(item)
                if value is not None:
                    output.append(value)
        else:
            output = None
            for item in self.items:
                value = self.map(item)
                if value is not None and find == value:
                    output = value
        return output

    def list(self):
        raise NotImplementedError

    def map(self, item):
        return item
