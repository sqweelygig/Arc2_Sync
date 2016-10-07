from bin.Factory import Factory


class GoogleStudent(Factory):
    def __init__(self, connection, item_settings, domain):
        try:
            super().__init__(connection, item_settings)
        except NotImplementedError:
            pass
        self.domain = domain

    @staticmethod
    def get_requirements():
        return Factory.get_requirements() | {"domain"}

    def get(self):
        return self.connection.list("student", domain=self.domain)
