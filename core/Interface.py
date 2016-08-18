from time import sleep
from time import time
from getpass import getpass
from unittest import TestCase
from functools import partial


class Interface:
    """
    An interface is for interacting with the user (or log?)
    It must contain methods:
    put(self, value) to output a string to the user
    get(self, key) to ask a question of the user
    reassure(self, value) to put an output to the user occasionally
    """
    def __init__(self):
        raise NotImplementedError()

    def put(self, value):
        raise NotImplementedError()

    def get(self, key):
        raise NotImplementedError()

    def reassure(self, value):
        raise NotImplementedError()


class InterfaceText(Interface):
    """
    This interfaces with the command line, by default using print, get_pass and input methods,
    but alternatives may be provided for testing purposes
    """
    def __init__(self, input_standard=None, input_obfuscated=None, output_standard=None):
        try:
            super().__init__()
        except NotImplementedError:
            pass
        self.interacted = False
        self.last_reassurance = False
        self.input_standard = input_standard if callable(input_standard) else input
        self.input_obfuscated = input_obfuscated if callable(input_obfuscated) else partial(getpass, "")
        self.output_standard = output_standard if callable(output_standard) else print

    def put(self, value):
        self.output_standard(value)
        sleep(self.interacted * 0.2)

    def get(self, key, interacted=True):
        self.interacted = interacted or self.interacted
        self.output_standard(key + '?')
        return self.input_obfuscated() if "password" in key else self.input_standard()

    def reassure(self, value):
        if self.last_reassurance is False or time() > self.last_reassurance + 0.7:
            if len(str(value)) > 60:
                value = str(value)[0:57] + '...'
            # so the output clears each time it just returns the carriage (\r), not new line (\n)
            self.output_standard(' ' * 60, end='\r')
            self.output_standard(value, end='\r')
            self.last_reassurance = time()

    def __del__(self):
        sleep(self.interacted * 60)


class TextTestCase(TestCase):
    def __init__(self, *positional, **keyword):
        super().__init__(*positional, **keyword)
        self.last_output = ""

    # noinspection PyUnusedLocal
    def catchOutput(self, value, end=None):
        self.last_output = value

    def setUp(self):
        self.interface = InterfaceText(
            input_standard=lambda: "standard",
            input_obfuscated=lambda: "obfuscated",
            output_standard=self.catchOutput
        )

    def testGetSimple(self):
        self.assertEqual("standard", self.interface.get("Just some string", False))

    def testGetPassword(self):
        self.assertEqual("obfuscated", self.interface.get("Just some string containing password", False))

    def testPutSimple(self):
        self.interface.put("test")
        self.assertEqual("test", self.last_output)

    def testReassureSimple(self):
        sleep(0.8)
        self.interface.reassure("a")
        sleep(0.8)
        self.assertEqual("a", self.last_output)

    def testReassureSequential(self):
        sleep(0.8)
        self.interface.reassure("b")
        sleep(0.8)
        self.interface.reassure("c")
        self.interface.reassure("d")
        sleep(0.8)
        self.assertEqual("c", self.last_output)

    def testReassureLong(self):
        sleep(0.8)
        self.interface.reassure("This string is really long, it needs to be at least 60 characters.")
        sleep(0.8)
        self.assertEqual("This string is really long, it needs to be at least 60 ch...", self.last_output)

