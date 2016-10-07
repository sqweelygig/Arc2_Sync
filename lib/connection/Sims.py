from bin.Connection import Connection


class Sims(Connection):
    @staticmethod
    def get_requirements():
        return Connection.get_requirements() | {"username", "password"}

    def __init__(self, interface, username, password):
        try:
            super().__init__(interface)
        except NotImplementedError:
            pass
