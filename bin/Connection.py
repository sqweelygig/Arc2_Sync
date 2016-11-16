def get_requirements(name):
    from lib.aliases import alias
    from importlib import import_module
    name = alias(name)
    module = import_module("lib.connection." + name)
    return getattr(module, name).get_requirements()


def build_connection(name, interface, root_dir, settings):
    from lib.aliases import alias
    from importlib import import_module
    from os import path
    name = alias(name)
    module = import_module("lib.connection." + name)
    return getattr(module, name)(interface, path.join(root_dir, name), **settings)


class Connection:
    @staticmethod
    def get_requirements():
        return set()

    def __init__(self, interface, root_dir):
        from os import makedirs
        from os import path
        self.interface = interface
        self.root_dir = root_dir
        if not path.exists(self.root_dir):
            makedirs(self.root_dir)
        # Abstract class
        raise NotImplementedError()

    def build_factory(self, name, factory_settings, item_settings):
        from lib.aliases import alias
        from importlib import import_module
        connection_name = type(self).__name__
        item_name = alias(name)
        name = connection_name + item_name
        module = import_module("lib.factory." + name)
        return getattr(module, name)(self, self.interface, item_settings, **factory_settings)


# from functools import partial
# from datetime import datetime
# from unittest import TestCase
#
#
# class Endpoint:
#     """
#     An connection abstracts the details of a data store and means accessing it can happen in a consistent fashion.
#     _get_<key>: returns a iterable of Items, may take advantage of _get_generic(list, map, filter, factory)
#     """
#
#
# class Model:
#     """
#     A model is for abstracting the details of a data store into a standardised fashion
#     A model must contain the following methods:
#     _list_<key>(self) for any key's that it is capable of getting from whatever data store it is abstracting
#     A model may contain the following methods:
#     _create_<key>(self, value) which will create a record
#     _update_<key>(self, value) which will update the record
#     _delete_<key>(self, value) which will delete the record
#     _map_<key>(value) which will return a standardised version of the value
#     _filter_<key>(value) which will return whether the provided value is of the key
#     _unmap_<key>(value)??? which will turn a standardised value into a specific version
#     """
#     requirements = set()
#     capabilities = {}
#
#     @staticmethod
#     def _map_generic(value, translations):
#         output = {}
#         for field in iter(translations):
#             if isinstance(translations.get(field), str):
#                 # If we've a leaf node
#                 if hasattr(value, "find"):
#                     # Use xml-style addressing
#                     node = value.find(translations.get(field))
#                 else:
#                     # Use dictionary style addressing
#                     node = value[translations.get(field)]
#                 if node is not None:
#                     if hasattr(node, "text"):
#                         # Use xml-style wrapping
#                         output[field] = node.text
#                     else:
#                         # Use plain value wrapping
#                         output[field] = node
#             else:
#                 # Recurse down the structure
#                 output[field] = Model._map_generic(value, translations.get(field))
#         return output
#
#     @staticmethod
#     def _pair(values):
#         pairs = []
#         keys_done = []
#         keys_to_do = []
#         for key in values:
#             keys_to_do.append(key)
#         while len(keys_to_do) > 0:
#             focus = keys_to_do.pop()
#             for key in iter(keys_to_do):
#                 for a_value in iter(values[focus]):
#                     match = Model._find(a_value, values[key])
#                     pairs.append({focus: a_value, key: match})
#             for key in iter(keys_done):
#                 for b_value in iter(values[focus]):
#                     match = Model._find(b_value, values[key])
#                     if match is None:
#                         pairs.append({key: match, focus: b_value})
#             keys_done.append(focus)
#         return pairs
#
#     @staticmethod
#     def _find(needle, haystack):
#         match = None
#         for straw in iter(haystack):
#             if match is None:
#                 if straw == needle:
#                     match = straw
#         return match
#
#     def __init__(self, interface=None, factories=None, settings=None):
#         self.settings = settings
#         self.factories = factories
#         self.interface = interface
#         self.name = self.__class__.__name__[5:].lower()
#         self.cache = {}
#
#     def get(self, key):
#         if key not in self.cache:
#             self.advertise("get", key)
#             buffer = getattr(self, "_list_" + key)()
#             buffer = map(partial(self._map, key), buffer)
#             buffer = filter(partial(self._filter, key), buffer)
#             factory = self.factories[key]
#             self.cache[key] = []
#             for value in buffer:
#                 self.cache[key].append(factory.build(value))
#         return self.cache[key]
#
#     def put(self, mode, key, values):
#         self.advertise(mode, key)
#         pairs = self._pair({"update": values, "existing": self.get(key)})
#         if mode in {'check', 'fix', 'tweak', 'sync'}:
#             for pair in pairs:
#                 getattr(self, "_" + mode)(key, pair["update"], pair["existing"])
#                 if pair["update"] is not None and pair["existing"] is not None and pair["update"] == pair["existing"]:
#                     pair["update"].extract(pair["existing"])
#
#     def _check(self, key, update, existing):
#         self._sync(key, update, existing, False)
#
#     def _fix(self, key, update, existing, do=True):
#         if existing is None and hasattr(self, "_update_" + key):
#             identifier = self.interface.get("?: " + str(update.details))
#             if identifier != "":
#                 self.interface.put("U: " + identifier + " > " + str(update.details))
#                 if do:
#                     getattr(self, "_update_" + key)(identifier, update)
#
#     def _tweak(self, key, update, existing, do=True):
#         if existing is not None and update is not None and hasattr(self, "_update_" + key):
#             if update.can_enrich(existing, self.capabilities[key]):
#                 self.interface.put(
#                     "U: " +
#                     existing.get_identifier() +
#                     " : " +
#                     str(existing.details) +
#                     " > " +
#                     str(update.details)
#                 )
#                 if do:
#                     getattr(self, "_update_" + key)(existing, update)
#
#     def _sync(self, key, update, existing, do=True):
#         if existing is not None and update is not None and hasattr(self, "_delete_" + key):
#             self._tweak(key, update, existing, do)
#         elif update is None and hasattr(self, "_delete_" + key):
#             if "used" not in existing.details or (datetime.now() - existing.details["used"]).days > 100:
#                 self.interface.put("D: " + existing.get_identifier())
#                 if do:
#                     getattr(self, "_delete_" + key)(existing)
#         elif existing is None and hasattr(self, "_create_" + key):
#             for field in self.capabilities[key]:
#                 if field not in update.details:
#                     while self.reject(field, update.suggest(field)):
#                         pass
#             self.interface.put("C: " + str(update.details))
#             if do:
#                 getattr(self, "_create_" + key)(update)
#
#     def reject(self, key, value):
#         if hasattr(self, "_reject_" + key):
#             return getattr(self, "_reject_" + key)(value)
#         else:
#             return False
#
#     def advertise(self, verb, key):
#         self.interface.put(
#             verb + " " +
#             self.name + " " +
#             key
#         )
#
#     def _filter(self, key, value):
#         if hasattr(self, "_filter_" + key):
#             output = getattr(self, "_filter_" + key)(value)
#         else:
#             output = True
#         return output
#
#     def _map(self, key, value):
#         # If we have specific map for this key
#         if hasattr(self, "_map_" + key):
#             # If the map is a method
#             if callable(getattr(self, "_map_" + key)):
#                 output = getattr(self, "_map_" + key)(value)
#             # If the map is an array
#             else:
#                 output = Model._map_generic(value, getattr(self, "_map_" + key))
#         # If we don't have a specific map for this key
#         else:
#             output = {}
#             for field in iter(value):
#                 # Pull across any xml nodes
#                 if hasattr(field, "tag"):
#                     output[field.tag] = field.text
#                 # Pull across any dictionary entries
#                 else:
#                     output[field] = value[field]
#         return output
#
#
# def get_model(key):
#     name = 'Model' + key[0].upper() + key[1:].lower()
#     m = __import__(name)
#     m = getattr(m, name)
#     return m
#
#
# class PairTest(TestCase):
#     def test(self):
#         self.maxDiff = None
#         self.assertEqual(Model._pair({}), [])
#         self.assertEqual(
#             Model._pair({
#                 'existing': [
#                     {'ids': {'test': 1}}
#                 ],
#                 'update': [
#                     {'ids': {'test': 1}}
#                 ]
#             }),
#             [
#                 {'existing': {'ids': {'test': 1}}, 'update': {'ids': {'test': 1}}}
#             ]
#         )
#         self.assertEqual(
#             Model._pair({
#                 'existing': [
#                     {'ids': {'test': 1}},
#                     {'ids': {'test': 2}}
#                 ],
#                 'update': [
#                     {'ids': {'test': 1}},
#                     {'ids': {'test': 3}}
#                 ]
#             }),
#             [
#                 {'existing': {'ids': {'test': 1}}, 'update': {'ids': {'test': 1}}},
#                 {'existing': None, 'update': {'ids': {'test': 3}}},
#                 {'existing': {'ids': {'test': 2}}, 'update': None}
#             ]
#         )
#         self.assertEqual(
#             Model._pair({
#                 'existing': [
#                     {'ids': {'test': 1}},
#                     {'ids': {'test': 2}}
#                 ],
#                 'update': [
#                     {'ids': {'test': 1}},
#                     {'ids': {'test': 3}}
#                 ],
#                 'extra': [
#                     {'ids': {'test': 1}}
#                 ]
#             }),
#             [
#                 {'existing': {'ids': {'test': 1}}, 'extra': {'ids': {'test': 1}}},
#                 {'update': {'ids': {'test': 1}}, 'extra': {'ids': {'test': 1}}},
#                 {'existing': {'ids': {'test': 1}}, 'update': {'ids': {'test': 1}}},
#                 {'existing': None, 'update': {'ids': {'test': 3}}},
#                 {'update': {'ids': {'test': 3}}, 'extra': None},
#                 {'existing': {'ids': {'test': 2}}, 'extra': None},
#                 {'existing': {'ids': {'test': 2}}, 'update': None}
#             ]
#         )
