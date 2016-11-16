from bin.Factory import Factory


class GoogleBase(Factory):
    def fetch(self):
        return self.connection.list(**self.get_list_arguments())

    def patch(self, item):
        self.connection.patch(**self.get_patch_arguments(item))

    def delete(self, item):
        raise NotImplementedError

    def put(self, item):
        self.connection.insert(**self.get_put_arguments(item))

    def get_list_arguments(self):
        # Abstract method
        raise NotImplementedError

    def get_patch_arguments(self, item):
        # Abstract method
        raise NotImplementedError

    def get_delete_arguments(self, item):
        # Abstract method
        raise NotImplementedError

    def get_put_arguments(self, item):
        # Abstract method
        raise NotImplementedError

    def __init__(self, connection, interface, settings):
        super().__init__(connection, interface, settings)

    def map(self, item):
        return item

    def unmap(self, item):
        return item


class GoogleBasePatch(GoogleBase):
    def get_put_arguments(self, item):
        raise NotImplementedError

    def get_list_arguments(self):
        raise NotImplementedError

    def get_patch_arguments(self, item):
        raise NotImplementedError

    def get_delete_arguments(self, item):
        raise NotImplementedError

    def delete(self, item):
        self.connection.patch(**self.get_delete_arguments(item))


class GoogleBaseDelete(GoogleBase):
    def get_put_arguments(self, item):
        raise NotImplementedError

    def get_list_arguments(self):
        raise NotImplementedError

    def get_patch_arguments(self, item):
        raise NotImplementedError

    def get_delete_arguments(self, item):
        raise NotImplementedError

    def delete(self, item):
        self.connection.delete(**self.get_delete_arguments(item))
