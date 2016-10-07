def build_interface(name):
    from aliases import alias
    name = alias(name)

    from importlib import import_module
    return getattr(
        import_module("lib.interface." + name),
        name
    )()


class Interface:
    """
    An interface is for interacting with external resource
    It must contain methods:
    put(self, output) to output a string
    get(self, key) to ask a question
    reassure(self, output) to output occasionally
    """

    def __init__(self):
        raise NotImplementedError()

    def put(self, output=""):
        raise NotImplementedError()

    def get(self, key=""):
        raise NotImplementedError()

    def reassure(self, output=""):
        raise NotImplementedError()


class InterfaceAntiWhizz(Interface):
    """
    An anti-whizz interface is for interacting with external resources
    It will delay or skip the standard methods, if required, to prevent whizz
    It must contain methods:
    _put(self, output) to output a string
    _get(self, output) to ask a question
    """

    last_interacted = False
    verbosity_options = {
        "nervous":   {"put": 0.4, "reassure":  2.5, "end": 600},
        "high":      {"put": 0.4, "reassure":  2.5, "end": 600},
        "default":   {"put": 0.2, "reassure":  5.0, "end":  60},
        "confident": {"put": 0.1, "reassure": 10.0, "end":   6},
        "low":       {"put": 0.1, "reassure": 10.0, "end":   6},
        "zero":      {"put": 0.0, "reassure": 30.0, "end":   0},
        "test":      {"put": 0.0, "reassure":  0.1, "end":   0},
    }
    verbosity = {"put": 0.2, "reassure": 5.0, "end": 60}

    def __init__(self, verbosity="default"):
        try:
            super().__init__()
        except NotImplementedError:
            pass
        self.verbosity = self.verbosity_options.get(verbosity)
        raise NotImplementedError()

    def put(self, output=""):
        from time import time
        while time() < self.last_interacted + self.verbosity.get("put"):
            pass
        self.last_interacted = time()
        self._put(output)

    def _put(self, output=""):
        raise NotImplementedError()

    def get(self, key=""):
        from time import time
        value = self._get(key)
        self.last_interacted = time()
        return value

    def _get(self, key=""):
        raise NotImplementedError()

    def reassure(self, output=""):
        from time import time
        if time() > self.last_interacted + self.verbosity.get("reassure"):
            self.last_interacted = time()
            self._put(output)

    def __del__(self):
        from time import sleep
        sleep(self.verbosity.get("end"))
