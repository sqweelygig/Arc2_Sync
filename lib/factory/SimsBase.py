from bin.Factory import FactoryReadOnly


class SimsBase(FactoryReadOnly):
    def __init__(self, connection, interface, item_settings):
        try:
            super().__init__(connection, interface, item_settings)
        except NotImplementedError:
            pass
        self.items = None

    def fetch(self):
        raise NotImplementedError

    def map(self, item):
        return item
