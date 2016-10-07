from bin.Item import Item


class Student(Item):
    def __init__(self):
        try:
            super().__init__()
        except NotImplementedError:
            pass
        raise NotImplementedError()
