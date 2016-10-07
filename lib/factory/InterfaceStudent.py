from bin.Factory import Factory


class InterfaceStudent(Factory):
    def __init__(self, connection, settings):
        try:
            super().__init__(connection, settings)
        except NotImplementedError:
            pass

    def get(self):
        return []
