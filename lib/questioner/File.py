from importlib import import_module
from unittest import TestCase

from bin.Questioner import Questioner


class File(Questioner):
    def __init__(self, filename="default"):
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


class FileTestCase(TestCase):
    def setUp(self):
        self.settings_getter = File("Test")

    def test_get(self):
        self.assertEqual("value", self.settings_getter.get("key"))
