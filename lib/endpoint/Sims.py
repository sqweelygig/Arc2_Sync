from bin.Endpoint import Endpoint

requirements = ["username", "password"]


class Sims(Endpoint):
    def __init__(self, interface, username, password):
        try:
            super().__init__(interface)
        except NotImplementedError:
            pass
