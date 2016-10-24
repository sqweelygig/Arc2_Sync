def get_requirements(connection_name, item_name):
    from lib.aliases import alias
    from importlib import import_module
    connection_name = alias(connection_name)
    item_name = alias(item_name)
    name = connection_name + item_name
    try:
        module = import_module("lib.factory." + name)
        return getattr(module, name).get_requirements()
    except ImportError:
        return Factory.get_requirements()


class FactoryReadOnly:
    def __init__(self, connection, item_settings):
        self.connection = connection
        self.item_settings = item_settings
        raise NotImplementedError

    @staticmethod
    def get_requirements():
        return set()

    def get(self):
        raise NotImplementedError


class Factory(FactoryReadOnly):
    def __init__(self, connection, item_settings):
        try:
            super().__init__(connection, item_settings)
        except NotImplementedError:
            pass
        raise NotImplementedError

    def get(self):
        raise NotImplementedError

    def put(self, item):
        raise NotImplementedError

    def delete(self, item):
        raise NotImplementedError

    def patch(self, item):
        raise NotImplementedError
