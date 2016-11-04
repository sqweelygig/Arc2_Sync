from bin.Connection import Connection


class Interface(Connection):
    def __init__(self, interface, root_dir):
        try:
            super().__init__(interface, root_dir)
        except NotImplementedError:
            pass

    def build_factory(self, name, factory_settings, item_settings):
        from lib.factory.InterfaceBase import InterfaceBase
        return InterfaceBase(self, self.interface, item_settings)
