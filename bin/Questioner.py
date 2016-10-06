import re


class Questioner:
    """
    Gathers settings from one of any number of sources
    A settings class will contain methods:
    _get(self, key) return the value[] associated with the provided key
    """

    def __init__(self):
        self.cache = {}
        raise NotImplementedError()

    def get(self, key, criteria='^.+$'):
        if key not in self.cache:
            self.cache[key] = self._get(key)
        if self.cache[key] is None or re.search(criteria, self.cache[key]) is None:
            raise KeyError()
        return self.cache[key]

    def get_many(self, keys):
        out = {}
        for key in iter(keys):
            out[key] = self.get(key)
        return out

    def _get(self, key):
        raise NotImplementedError()


class QuestionerDictionary(Questioner):
    """
    Stores settings in a dictionary, which should be provided in the constructor
    """

    def __init__(self, dictionary=None):
        try:
            super().__init__()
        except NotImplementedError:
            pass
        self.dictionary = {} if dictionary is None else dictionary

    def _get(self, key):
        return self.dictionary.get(key)
