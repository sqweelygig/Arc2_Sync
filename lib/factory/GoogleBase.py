from bin.Factory import Factory


class GoogleBase(Factory):
    def patch(self, item):
        # TODO Implement
        print("U:" + str(item.ids))

    def delete(self, item):
        # TODO Implement
        print("D:" + str(item.ids))

    def put(self, item):
        # TODO Implement
        print("C:" + str(item.ids))

    def get(self):
        items = self.connection.list(**self.get_list_arguments())
        output = []
        for item in items:
            value = self.map(item)
            if value is not None:
                output.append(value)
        return output

    def get_list_arguments(self):
        raise NotImplementedError

    def __init__(self, connection, settings):
        super().__init__(connection, settings)

    @staticmethod
    def map(item):
        return item
