from bin.Item import Item


class Supervisor(Item):
    def __init__(self, ids, details=None, partial=False):
        try:
            super().__init__(ids, details, partial)
        except NotImplementedError:
            pass
