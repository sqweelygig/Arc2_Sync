from googleapiclient.errors import HttpError
from bin.Item import Item
from lib.factory.GoogleBase import GoogleBase
from lib.factory.GoogleStaff import GoogleStaff


class GoogleAlias(GoogleBase):
    def get_list_arguments(self):
        return {
            "endpoint": "classroom",
            "version": "v1",
            "path": ["courses", "aliases"],
            "key": "aliases",
            "courseId": self.course_id
        }

    def get_delete_arguments(self, item):
        raise NotImplementedError

    def get_patch_arguments(self, item):
        raise NotImplementedError

    def get_put_arguments(self, item):
        raise NotImplementedError

    def map(self, item):
        item = super().map(item)
        item = {
            "ids": {},
            "details": {
                item["alias"].split(':')[1]: item["alias"].split(':')[-1]
            },
        }
        return Alias(**item)

    @staticmethod
    def get_requirements():
        return GoogleBase.get_requirements() | {"course_id"}

    def __init__(self, connection, item_settings, course_id):
        try:
            super().__init__(connection, item_settings)
        except NotImplementedError:
            pass
        self.course_id = course_id


class Alias(Item):
    def __init__(self, ids, details=None, partial=False):
        try:
            super().__init__(ids, details, partial)
        except NotImplementedError:
            pass


# TODO Make this understand archived
class GoogleCourse(GoogleBase):
    def __init__(self, connection, item_settings, domain):
        try:
            super().__init__(connection, item_settings)
        except NotImplementedError:
            pass
        self.sub_factories = {
            "staff": GoogleStaff(connection, {}, domain),
        }

    @staticmethod
    def get_requirements():
        return GoogleStaff.get_requirements()

    @staticmethod
    def get_common_arguments():
        return {
            "endpoint": "classroom",
            "version": "v1",
            "path": ["courses"],
        }

    def get_list_arguments(self):
        return {
            **self.get_common_arguments(),
            "key": "courses",
        }

    def get_patch_arguments(self, item):
        return {
            **self.get_common_arguments(),
            "id": "p:sims:course:"+item.ids["sims"],
            "updateMask": "courseState",
            "body": {
                "courseState": "PROVISIONED",
            },
        }

    def get_put_arguments(self, item):
        return {
            **self.get_common_arguments(),
            "body": self.unmap(item),
        }

    def get_delete_arguments(self, item):
        return {
            **self.get_common_arguments(),
            "id": item.ids["google"],
            "updateMask": "courseState",
            "body": {
                "courseState": "ARCHIVED",
            },
        }

    def put(self, item):
        try:
            super().put(item)
        except HttpError:
            super().patch(item)

    def unmap(self, item):
        item.details["teacher"] = self.sub_factories["staff"].get(item.details["teacher"])
        output = {
            # TODO make this line understand multiple origins
            "id": "p:sims:course:"+item.ids["sims"],
            "name": item.details["name"],
            "ownerId": item.details["teacher"].ids["google"],
        }
        return output

    def map(self, item):
        from lib.item.Course import Course
        from lib.item.Staff import Staff
        item = super().map(item)
        if item["courseState"] in {"ARCHIVED"}:
            return None
        else:
            aliases_factory = GoogleAlias(self.connection, {}, item["id"])
            item = {
                "ids": {
                    "google": item["id"]
                },
                "details": {
                    "name": item["name"],
                    "teacher": self.sub_factories["staff"].get(
                        Staff(ids={"google": item["ownerId"]}, partial=True)
                    )
                }
            }
            for alias in aliases_factory.list():
                item["ids"] = {**item["ids"], **alias.details}
            if "sims" in item["ids"]:
                return Course(**item)
            else:
                return None

    def can_update(self, update):
        return super()._can_update(update, (), ("name", "teacher"))
