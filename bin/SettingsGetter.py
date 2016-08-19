from sys import argv
from copy import copy
from unittest import TestCase
# noinspection PyUnresolvedReferences
from Interface import InterfaceText
from importlib import import_module


class SettingsGetter:
    """
    A settings object is for gathering settings from one of any number of sources
    A settings class will contain methods:
    _get(self, key) return the value[] associated with the provided key
    """

    def __init__(self):
        self.cache = {}
        raise NotImplementedError()

    def get(self, key):
        if key not in self.cache:
            self.cache[key] = self._get(key)
        return copy(self.cache[key])

    def get_many(self, keys):
        out = {}
        for key in iter(keys):
            out[key] = self.get(key)
        return out

    def get_cache(self):
        out = {}
        for key, value in iter(self.cache):
            out[key] = copy(value)
        return out

    def clear_cache(self):
        self.cache = {}

    def _get(self, key):
        raise NotImplementedError()


class SettingsGetterArgs(SettingsGetter):
    def __init__(self, arguments=None):
        try:
            super().__init__()
        except NotImplementedError:
            pass
        self.args = self._process_arguments(argv if arguments is None else arguments)

    @staticmethod
    def _process_arguments(arguments):
        out = {}
        key = None
        for value in iter(arguments[1:]):
            if value[0] == '-':
                key = value[1:]
            elif key in out:
                out[key].append(value)
            else:
                out[key] = [value]
        return out

    def _get(self, key):
        return self.args[key]


class SettingsGetterCombiner(SettingsGetter):
    def __init__(self, sources):
        try:
            super().__init__()
        except NotImplementedError:
            pass
        self.sources = sources

    def _get(self, key):
        out = None
        for source in iter(self.sources):
            if out is None:
                try:
                    out = source.get(key)
                except KeyError:
                    pass
        if out is None:
            raise KeyError
        else:
            return out


class SettingsGetterInterface(SettingsGetter):
    def __init__(self, interface):
        try:
            super().__init__()
        except NotImplementedError:
            pass
        self.interface = interface

    def _get(self, key):
        return [self.interface.get(key)]


class SettingsGetterFile(SettingsGetter):
    def __init__(self, filename="main"):
        try:
            super().__init__()
        except NotImplementedError:
            pass
        self.module = import_module("config."+filename[0].upper()+filename[1:].lower())

    def _get(self, key):
        if hasattr(self.module, key):
            return getattr(self.module, key)
        else:
            raise KeyError


class ArgsTestCase(TestCase):
    def setUp(self):
        self.settings_getter = SettingsGetterArgs(
            arguments=("script.py", "-test", "this", "-second", "that", "-array", "first", "second")
        )

    def testGet(self):
        self.assertEqual(["this"], self.settings_getter.get("test"))
        self.assertEqual(["that"], self.settings_getter.get("second"))

    def testGetMany(self):
        self.assertEqual({"test": ["this"], "second": ["that"]}, self.settings_getter.get_many(("test", "second")))

    def testGetArray(self):
        self.assertEqual(["first", "second"], self.settings_getter.get("array"))


class InterfaceTestCase(TestCase):
    def setUp(self):
        interface = InterfaceText(
            input_standard=lambda: "standard",
            input_obfuscated=lambda: "obfuscated",
            output_standard=lambda x: x
        )
        self.settings_getter = SettingsGetterInterface(interface=interface)

    def testGet(self):
        self.assertEqual(["standard"], self.settings_getter.get("test"))
        self.assertEqual(["obfuscated"], self.settings_getter.get("password"))

    def testGetMany(self):
        self.assertEqual(
            {"test": ["standard"], "password": ["obfuscated"]},
            self.settings_getter.get_many(("test", "password"))
        )


class FileTestCase(TestCase):
    def setUp(self):
        self.settings_getter = SettingsGetterFile("test")

    def testGet(self):
        self.assertEqual(["value"], self.settings_getter.get("key"))


class CombinerTestCase(TestCase):
    def setUp(self):
        a = SettingsGetterArgs(arguments=("script.py", "-a", "a"))
        b = SettingsGetterArgs(arguments=("script.py", "-b", "b"))
        self.settings_getter = SettingsGetterCombiner(sources=(a, b))

    def testGet(self):
        self.assertEqual(["a"], self.settings_getter.get("a"))
        self.assertEqual(["b"], self.settings_getter.get("b"))

    def testGetMany(self):
        self.assertEqual({"a": ["a"], "b": ["b"]}, self.settings_getter.get_many(("a", "b")))
