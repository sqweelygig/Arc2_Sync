from bin.Factory import Factory


class GoogleBase(Factory):
    def patch(self, item):
        self.connection.patch(body=self.unmap(item, "patch"), **self.get_patch_arguments(item))

    def delete(self, item):
        self.connection.delete(**self.get_delete_arguments(item))

    def put(self, item):
        # TODO Implement
        print("!C:" + str(item.ids))

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

    def get_patch_arguments(self, item):
        raise NotImplementedError

    def get_delete_arguments(self, item):
        raise NotImplementedError

    def __init__(self, connection, settings):
        super().__init__(connection, settings)

    @staticmethod
    def map(item):
        return item

    @staticmethod
    def unmap(item, purpose=None):
        return item
