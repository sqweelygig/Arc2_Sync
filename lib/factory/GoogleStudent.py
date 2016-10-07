from bin.Factory import Factory


class GoogleStudent(Factory):
    def __init__(self, connection, settings, domain):
        try:
            super().__init__(connection, settings)
        except NotImplementedError:
            pass
        self.domain = domain

    @staticmethod
    def get_requirements():
        return Factory.get_requirements() | {"domain"}
