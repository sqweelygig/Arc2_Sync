def get_requirements(name):
    from aliases import alias
    from importlib import import_module
    name = alias(name)
    module = import_module("lib.item." + name)
    return getattr(module, name).get_requirements()


class Item:
    @staticmethod
    def get_requirements():
        return set()

    def __init__(self, ids, details):
        for key in self.get_core_fields():
            if details[key] is None:
                raise IndexError
        self.ids = ids
        self.details = details
        raise NotImplementedError()

    def __eq__(self, other):
        for key, value in self.ids.items():
            if other.ids.get(key) == value:
                return True
        return False

    def __str__(self):
        return self.ids.__str__()

    def enrich(self, other):
        enriched = False
        for key in other.ids:
            if self.ids.get(key) != other.ids.get(key):
                enriched = enriched or key in self.ids
        for key in other.details:
            # TODO The logic of these two lines is not pretty, but works.  I'd like them to be both.
            if self.details.get(key) != other.details.get(key):
                enriched = enriched or (key in self.details) or (key in self.get_core_fields())
                self.details[key] = other.details[key]
        return enriched

    @staticmethod
    def get_core_fields():
        return set()


# from importlib import import_module
# from unittest import TestCase
#
# # TODO upfront settings => items must advertise both their settings, and any sub-items they rely upon
#
#
# class Factory:
#     def __init__(self, item_name, settings_getter=None):
#         self.item_class = self._find_item_class(item_name)
#         if len(self.item_class.requirements) > 0:
#             if settings_getter is None:
#                 raise Exception
#             else:
#                 self.settings = settings_getter.get_many(self.item_class.requirements)
#
#     @staticmethod
#     def _find_item_class(item_name):
#         name = "Item" + item_name[0].upper() + item_name[1:].lower()
#         try:
#             m = import_module("lib."+name+'.'+name)
#             i = getattr(m, name) if hasattr(m, name) else Item
#         except ImportError:
#             i = Item
#         return i
#
#     def build(self, ids, details=None):
#         return self.item_class(settings=self.settings, ids=ids, details=details or {})
#
#
# class Item:
#     requirements = set()
#
#     def __init__(self, settings, ids, details):
#         self.settings = settings
#         self.ids = ids
#         self.details = details
#
#     def __str__(self):
#         output = {
#             "ids": self.ids,
#             "details": self.details
#         }
#         return str(output)
#
#     def __eq__(self, other):
#         for key in iter(self.ids):
#             if key in other.ids and other.ids[key] == self.ids[key]:
#                 # if one id matches
#                 return True
#         # if no ids match
#         return False
#
#     def __ne__(self, other):
#         return not self.__eq__(other)
#
#     def suggest(self, key):
#         return getattr(self, "_suggest_"+key)()
#
#     def enrich(self, other):
#         if other is not None and self == other:
#             for key in iter(other.ids):
#                 self.ids[key] = other.ids[key]
#             for key in iter(other.details):
#                 self.details[key] = other.details[key]
#
#
# class FactoryTestCase(TestCase):
#     def setUp(self):
#         self.factory_test = Factory("test")
#         self.factory_duff = Factory("invalid")
#
#     def testCorrectItem(self):
#         self.assertEqual("ItemTest", self.factory_test.item_class.__name__)
#         self.assertEqual("Item", self.factory_duff.item_class.__name__)
