from bin.Item import Item


class Student(Item):
    def __init__(self, ids, details):
        try:
            super().__init__(ids, details)
        except NotImplementedError:
            pass

    @staticmethod
    def get_core_fields():
        output = Item.get_core_fields()
        output.add("forename")
        output.add("surname")
        return output
