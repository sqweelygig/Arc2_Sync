from lib.factory.SimsBase import SimsBase


class SimsCourse(SimsBase):
    def __init__(self, connection, interface, item_settings):
        from lib.factory.SimsStaff import SimsStaff
        try:
            super().__init__(connection, interface, item_settings)
        except NotImplementedError:
            pass
        self.sub_factories = {
            "staff": SimsStaff(connection, interface, {})
        }

    def fetch(self):
        return self.connection.list("courses")

    def map(self, item):
        from lib.item.Course import Course
        from lib.item.Staff import Staff
        from _md5 import md5
        item = super().map(item)
        m = md5()
        m.update(item.find("NI_x0020_Number").text.encode("utf-8"))
        item = {
            "ids": {
                "sims": item.find("primary_id").text,
            },
            "details": {
                "name": item.find("Class").text,
                "teacher": self.sub_factories["staff"].get(
                    Staff(ids={"nihash": m.hexdigest()}, partial=True)
                )
            },
        }
        return Course(**item)
