from lib.factory.SimsBase import SimsBase


class SimsSupervisor(SimsBase):
    def __init__(self, connection, interface, item_settings):
        from lib.factory.SimsStaff import SimsStaff
        from lib.factory.SimsCourse import SimsCourse
        try:
            super().__init__(connection, interface, item_settings)
        except NotImplementedError:
            pass
        self.sub_factories = {
            "staff": SimsStaff(connection, interface, {}),
            "courses": SimsCourse(connection, interface, {}),
        }

    def fetch(self):
        return self.connection.list("supervisors")

    def map(self, item):
        from lib.item.Supervisor import Supervisor
        from lib.item.Course import Course
        from lib.item.Staff import Staff
        from _md5 import md5
        item = super().map(item)
        course_id = item.find("multiple_id").text.split(",")[0]
        m = md5()
        m.update(item.find("NI_x0020_Number").text.encode('utf-8'))
        staff_id = m.hexdigest()
        course = self.sub_factories["courses"].get(Course(ids={"sims": course_id}, partial=True))
        supervisor = self.sub_factories["staff"].get(Staff(ids={"nihash": staff_id}, partial=True))
        if supervisor is None or course is None:
            return None
        m = md5()
        m.update((course.ids["sims"] + ':' + supervisor.ids["sims"]).encode('utf-8'))
        item = {
            "ids": {"sims": m.hexdigest()},
            "details": {"supervisor": supervisor, "course": course},
        }
        return Supervisor(**item)
