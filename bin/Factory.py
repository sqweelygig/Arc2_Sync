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
    def __init__(self, connection, interface, item_settings):
        self.connection = connection
        self.item_settings = item_settings
        self.interface = interface
        self.items = None
        self.indexed_items = None
        # Abstract class
        raise NotImplementedError

    @staticmethod
    def get_requirements():
        return set()

    def get(self, find):
        if self.indexed_items is None:
            self.list()
        output = None
        for id_key in find.ids:
            output = output or self.indexed_items[id_key].get(find.ids[id_key], None)
        return output

    def list(self):
        if self.items is None:
            self.items = self.fetch()
        output = []
        self.indexed_items = {}
        for item in self.items:
            value = self.map(item)
            if value is not None:
                if len(value.ids) > 0:
                    append = False
                    for id_key in value.ids:
                        if self.indexed_items.get(id_key, None) is None:
                            self.indexed_items[id_key] = {}
                        if self.indexed_items[id_key].get(value.ids[id_key], None) is None:
                            self.indexed_items[id_key][value.ids[id_key]] = value
                            append = True
                    if append:
                        output.append(value)
                        self.interface.reassure(str(value))
                else:
                    output.append(value)
                    self.interface.reassure(str(value))
        return output

    def fetch(self):
        # Abstract method
        raise NotImplementedError

    def map(self, item):
        # Abstract method
        raise NotImplementedError

    def can_update(self, update):
        return self._can_update(update)

    @staticmethod
    def _can_update(update, ignore_ids=(), ignore_details=()):
        for key in update["ids"]:
            if key not in ignore_ids:
                return True
        for key in update["details"]:
            if key not in ignore_details:
                return True
        # Either update was empty or everything was in an ignore
        return False


class Factory(FactoryReadOnly):
    def __init__(self, connection, interface, item_settings):
        try:
            super().__init__(connection, interface, item_settings)
        except NotImplementedError:
            pass
        # Abstract class
        raise NotImplementedError

    def put(self, item):
        # Abstract method
        raise NotImplementedError

    def delete(self, item):
        # Abstract method
        raise NotImplementedError

    def patch(self, item):
        # Abstract method
        raise NotImplementedError

    def map(self, item):
        # Abstract method
        raise NotImplementedError

    def fetch(self):
        # Abstract method
        raise NotImplementedError
