from importlib.util import find_spec
from importlib import import_module
from unittest import TestCase

# Some notes
# username format => some things may come from a settingsGetter object
# multi-source, same entity => two items are the same if there is overlap in their ids
# multi-source, differing fields => items must facilitate gradual enrichment techniques
# incomplete source => items must be able to suggest field options
# upfront settings => items must advertise both their settings, and any sub-items they rely upon


class Factory:
    def __init__(self, item_name, settings_getter=None):
        # TODO something with sub classes
        self.item_class = self._find_item_class(item_name)
        if len(self.item_class.requirements) > 0:
            if settings_getter is None:
                raise Exception
            else:
                self.settings = settings_getter.get_many(self.item_class.requirements)

    @staticmethod
    def _find_item_class(item_name):
        name = "Item" + item_name[0].upper() + item_name[1:].lower()
        if find_spec("lib."+name) is not None:
            m = import_module("lib."+name)
            i = getattr(m, name) if hasattr(m, name) else Item
        else:
            i = Item
        return i

    def build(self, ids, details=None):
        return self.item_class(settings=self.settings, ids=ids, details=details or {})


class Item:
    requirements = set()
    sub_items = set()

    def __init__(self, settings, ids, details):
        self.settings = settings
        self.ids = {}
        self.ids = ids
        self.details = details


class FactoryTestCase(TestCase):
    def setUp(self):
        self.factory_test = Factory("test")
        self.factory_duff = Factory("blahblahblah")

    def testCorrectItem(self):
        self.assertEqual("ItemTest", self.factory_test.item_class.__name__)
        self.assertEqual("Item", self.factory_duff.item_class.__name__)

# def get_factory(key):
#     name = "lib."+'Item' + key[0].upper() + key[1:].lower()
#     if find_spec(name) is not None:
#         m = import_module(name)
#     else:
#         m = sys.modules[__name__]
#     f = getattr(m, "Factory") if hasattr(m, "Factory") else Factory
#     return f
#
# class Factory:
#     requirements = set()
#     sub_factories = set()
#
#     def __init__(self, item, interface, settings):
#         self.item = item
#         self.settings = settings
#         self.interface = interface
#
#     def build(self, value):
#         return self.item(
#             ids=value["ids"],
#             details=value["details"] if "details" in value else {}
#         )
#
#
# class Item:
#     def __init__(self, ids, details=None):
#         self.ids = ids
#         if details is None:
#             self.details = {}
#         else:
#             self.details = details
#         self.suggests = {}
#
#     def __str__(self):
#         output = {
#             'ids': self.ids,
#             'details': self.details
#         }
#         return str(output)
#
#     def __eq__(self, other):
#         for key in self.ids:
#             if key in other.ids and other.ids[key] == self.ids[key]:
#                 # if one id matches
#                 return True
#         # If no ids match
#         return False
#
#     def __ne__(self, other):
#         return not self.__eq__(other)
#
#     def get_identifier(self):
#         return str(self.ids)
#
#     def can_enrich(self, other, capabilities='All'):
#         if self != other:
#             # If there's no overlap of id
#             return False
#         if capabilities == 'All':
#             loop = self.details
#         else:
#             loop = capabilities
#         for detail in self.details:
#             if detail in loop:
#                 if detail in other.details:
#                     if other.details[detail] != self.details[detail]:
#                         # If one detail differs
#                         return True
#                 else:
#                     # If one detail is missing
#                     return True
#         for key in self.ids:
#             if key in other.ids:
#                 if other.ids[key] != self.ids[key]:
#                     # If one id differs
#                     return True
#             else:
#                 # If one id is missing
#                 return True
#         # All ids and details are identical
#         return False
#
#     def extract(self, other):
#         if other is not None and self == other:
#             for key in iter(other.ids):
#                 self.ids[key] = other.ids[key]
#             for key in iter(other.details):
#                 self.details[key] = other.details[key]
#
#     def suggest(self, key):
#         if key in self.suggests:
#             self.details[key] = self.suggests[key]()
#         return self.details[key]
