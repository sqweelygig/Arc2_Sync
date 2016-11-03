from bin.Factory import Factory


class GoogleBase(Factory):
    def fetch(self):
        return self.connection.list(**self.get_list_arguments())

    def patch(self, item):
        self.connection.patch(**self.get_patch_arguments(item))

    def delete(self, item):
        self.connection.patch(**self.get_delete_arguments(item))

    def put(self, item):
        self.connection.insert(**self.get_put_arguments(item))

    def get_list_arguments(self):
        raise NotImplementedError

    def get_patch_arguments(self, item):
        raise NotImplementedError

    def get_delete_arguments(self, item):
        raise NotImplementedError

    def get_put_arguments(self, item):
        raise NotImplementedError

    def __init__(self, connection, settings):
        super().__init__(connection, settings)

    def map(self, item):
        return item

    def unmap(self, item):
        return item
