from bin.Factory import Factory


# noinspection PyAbstractClass
class InterfaceBase(Factory):
    def __init__(self, connection, settings):
        try:
            super().__init__(connection, settings)
        except NotImplementedError:
            pass

    def get(self):
        return []
