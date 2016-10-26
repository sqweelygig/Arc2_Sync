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
        self.items = None
        raise NotImplementedError

    @staticmethod
    def get_requirements():
        return set()

    def get(self, find):
        output = None
        for item in self.list():
            if find == item:
                output = item
        return output

    def list(self):
        if self.items is None:
            self.items = self.fetch()
        output = []
        for item in self.items:
            value = self.map(item)
            if value is not None:
                output.append(value)
        return output

    def fetch(self):
        raise NotImplementedError

    def map(self, item):
        raise NotImplementedError

    def can_update(self, update):
        return len(update["ids"]) > 0 or len(update["details"]) > 0


class Factory(FactoryReadOnly):
    def __init__(self, connection, item_settings):
        try:
            super().__init__(connection, item_settings)
        except NotImplementedError:
            pass
        raise NotImplementedError

    def put(self, item):
        raise NotImplementedError

    def delete(self, item):
        raise NotImplementedError

    def patch(self, item):
        raise NotImplementedError

    def map(self, item):
        raise NotImplementedError

    def fetch(self):
        raise NotImplementedError
