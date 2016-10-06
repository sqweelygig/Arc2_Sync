from functools import partial
from getpass import getpass
from time import sleep
from unittest import TestCase

from bin.Interface import InterfaceAntiWhizz


class Text(InterfaceAntiWhizz):
    """
    An interface for interacting with the command line by default
    Can interact with other text based methods if setup correctly
    """

    input_standard = print
    input_obfuscated = partial(getpass, "")
    output_standard = print
    console_width = 60

    def __init__(self, verbosity="default", input_standard=None, input_obfuscated=None, output_standard=None):
        try:
            super().__init__(verbosity)
        except NotImplementedError:
            pass
        if callable(input_standard):
            self.input_standard = input_standard
        if callable(input_obfuscated):
            self.input_obfuscated = input_obfuscated
        if callable(output_standard):
            self.output_standard = output_standard

    def _put(self, output=""):
        self.output_standard(output)

    def _get(self, key=""):
        self.put(key+"?")
        return self.input_obfuscated() if "password" in key else self.input_standard()

    def reassure(self, output=""):
        if len(str(output)) > self.console_width:
            super().reassure(str(output)[0:self.console_width-3] + "...")
        else:
            super().reassure(output)


class TextTestCase(TestCase):
    def __init__(self, *positional, **keyword):
        super().__init__(*positional, **keyword)
        self.last_output = None

    def catch_output(self, value):
        self.last_output = value

    def setUp(self):
        self.interface = Text(
            input_standard=lambda: "standard",
            input_obfuscated=lambda: "obfuscated",
            output_standard=self.catch_output,
            verbosity="test"
        )

    def test_put_simple(self):
        self.interface.put("test")
        self.assertEqual("test", self.last_output)

    def test_get_simple(self):
        self.assertEqual("standard", self.interface.get("Just some string"))

    def test_get_password(self):
        self.assertEqual("obfuscated", self.interface.get("Just some string containing password"))

    def test_reassure_simple(self):
        sleep(0.2)
        self.interface.reassure("a")
        sleep(0.2)
        self.assertEqual("a", self.last_output)

    def test_reassure_sequential(self):
        sleep(0.2)
        self.interface.reassure("b")
        sleep(0.2)
        self.interface.reassure("c")
        self.interface.reassure("d")
        sleep(0.2)
        self.assertEqual("c", self.last_output)

    def test_reassure_long(self):
        sleep(0.2)
        self.interface.reassure("This string is really long, it needs to be at least 60 characters.")
        sleep(0.2)
        self.assertEqual("This string is really long, it needs to be at least 60 ch...", self.last_output)
