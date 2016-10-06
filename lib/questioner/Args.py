from sys import argv
from unittest import TestCase

from bin.Questioner import QuestionerDictionary


class Args(QuestionerDictionary):
    def __init__(self, arguments=None):
        try:
            super().__init__(dictionary=self._process_arguments(argv if arguments is None else arguments))
        except NotImplementedError:
            pass

    @staticmethod
    def _process_arguments(arguments):
        out = {}
        key = None
        for value in iter(arguments[1:]):
            if value[0] == '-':
                key = value[1:]
            else:
                out[key] = value
        return out


class ArgsTestCase(TestCase):
    def setUp(self):
        self.settings_getter = Args(
            arguments=("script.py", "-test", "this", "-second", "that", "-third", "first", "second")
        )

    def test_get(self):
        self.assertEqual("this", self.settings_getter.get("test"))
        self.assertEqual("that", self.settings_getter.get("second"))

    def test_get_many(self):
        self.assertEqual({"test": "this", "second": "that"}, self.settings_getter.get_many(("test", "second")))

    def test_get_overridden(self):
        self.assertEqual("second", self.settings_getter.get("third"))
