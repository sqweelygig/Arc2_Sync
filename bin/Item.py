def get_requirements(name):
    from lib.aliases import alias
    from importlib import import_module
    name = alias(name)
    module = import_module("lib.item." + name)
    return getattr(module, name).get_requirements()


class Item:
    @staticmethod
    def get_requirements():
        return set()

    def __init__(self, ids, details=None, partial=False):
        if details is None:
            details = {}
        if not partial:
            for key in self.get_core_fields():
                if details[key] is None:
                    raise IndexError
        self.ids = ids
        self.details = details
        # Abstract class
        raise NotImplementedError()

    def __eq__(self, other):
        if other is None:
            return False
        for key, value in iter(self.ids.items()):
            if other.ids.get(key) == value:
                return True
        return False

    def __repr__(self):
        return {
            "ids": self.ids,
            "details": self.details,
        }.__repr__()

    def enrich(self, other):
        updates = {
            "ids": [],
            "details": [],
        }
        for key in other.ids:
            if self.ids.get(key) != other.ids.get(key):
                updates["ids"].append(key)
                self.ids[key] = other.ids[key]
        for key in other.details:
            if self.details.get(key) != other.details.get(key):
                updates["details"].append(key)
                self.details[key] = other.details[key]
        return updates

    def get(self, key):
        if key not in self.details:
            self.details[key] = getattr(self, "suggest_" + key)()
        return self.details[key]

    @staticmethod
    def get_core_fields():
        return set()

