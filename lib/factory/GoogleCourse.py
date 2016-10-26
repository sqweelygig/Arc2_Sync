from lib.factory.GoogleBase import GoogleBase
from lib.factory.GoogleStaff import GoogleStaff


class GoogleCourse(GoogleBase):
    def __init__(self, connection, item_settings, domain):
        try:
            super().__init__(connection, item_settings)
        except NotImplementedError:
            pass
        self.domain = domain

    @staticmethod
    def get_requirements():
        return GoogleStaff.get_requirements()

    def get_list_arguments(self):
        return {
            "endpoint": "classroom",
            "version": "v1",
            "path": ["courses"],
            "key": "courses",
        }

    def get_patch_arguments(self, item):
        raise NotImplementedError

    def get_put_arguments(self, item):
        raise NotImplementedError

    def get_delete_arguments(self, item):
        raise NotImplementedError
