from bin.Connection import Connection


class Interface(Connection):
    def __init__(self, interface, root_dir):
        try:
            super().__init__(interface, root_dir)
        except NotImplementedError:
            pass
