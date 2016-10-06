from unittest import TestCase

from bin.Questioner import Questioner, QuestionerDictionary


class Combiner(Questioner):
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


class CombinerTestCase(TestCase):
    def setUp(self):
        a = QuestionerDictionary({"a": "a"})
        b = QuestionerDictionary({"b": "b", "a": "c"})
        self.settings_getter = Combiner(sources=(a, b))

    def test_get(self):
        self.assertEqual("a", self.settings_getter.get("a"))
        self.assertEqual("b", self.settings_getter.get("b"))

    def test_get_many(self):
        self.assertEqual({"a": "a", "b": "b"}, self.settings_getter.get_many(("a", "b")))
