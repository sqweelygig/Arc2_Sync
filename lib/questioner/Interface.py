from unittest import TestCase

from bin.Questioner import Questioner
from lib.interface.Text import Text


class Interface(Questioner):
    def __init__(self, interface):
        try:
            super().__init__()
        except NotImplementedError:
            pass
        self.interface = interface

    def _get(self, key):
        return self.interface.get(key)


class InterfaceTestCase(TestCase):
    def setUp(self):
        interface = Text(
            input_standard=lambda: "standard",
            input_obfuscated=lambda: "obfuscated",
            output_standard=lambda x: x,
            verbosity="test",
        )
        self.settings_getter = Interface(interface=interface)

    def test_get(self):
        self.assertEqual("standard", self.settings_getter.get("test"))
        self.assertEqual("obfuscated", self.settings_getter.get("password"))

    def test_get_many(self):
        self.assertEqual(
            {"test": "standard", "password": "obfuscated"},
            self.settings_getter.get_many(("test", "password"))
        )
