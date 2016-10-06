from bin.Endpoint import Endpoint


class Interface(Endpoint):
    def __init__(self, interface):
        try:
            super().__init__(interface)
        except NotImplementedError:
            pass
