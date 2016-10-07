from bin.Connection import Connection


class Interface(Connection):
    def __init__(self, interface):
        try:
            super().__init__(interface)
        except NotImplementedError:
            pass
