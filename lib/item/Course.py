from bin.Item import Item


class Course(Item):
    def __init__(self, ids, details=None, partial=False):
        try:
            super().__init__(ids, details, partial)
        except NotImplementedError:
            pass

    @staticmethod
    def get_core_fields():
        output = Item.get_core_fields()
        output.add("name")
        return output
