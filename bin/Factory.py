def get_requirements(connection_name, item_name):
    from aliases import alias
    from importlib import import_module
    connection_name = alias(connection_name)
    item_name = alias(item_name)
    name = connection_name + item_name
    module = import_module("lib.factory." + name)
    return getattr(module, name).get_requirements()


class Factory:
    def __init__(self, connection, item_settings):
        self.connection = connection
        self.item_settings = item_settings
        raise NotImplementedError

    @staticmethod
    def get_requirements():
        return set()

    def get(self):
        raise NotImplementedError
