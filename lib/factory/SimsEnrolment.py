from lib.factory.SimsBase import SimsBase


class SimsEnrolment(SimsBase):
    def __init__(self, connection, interface, item_settings):
        from lib.factory.SimsStudent import SimsStudent
        from lib.factory.SimsCourse import SimsCourse
        try:
            super().__init__(connection, interface, item_settings)
        except NotImplementedError:
            pass
        self.sub_factories = {
            "students": SimsStudent(connection, interface, {}),
            "courses": SimsCourse(connection, interface, {}),
        }

    def fetch(self):
        return self.connection.list("enrolments")

    def map(self, item):
        from lib.item.Enrolment import Enrolment
        from lib.item.Course import Course
        from lib.item.Student import Student
        from _md5 import md5
        item = super().map(item)
        course_id = item.find("multiple_id").text.split(",")[0]
        student_id = item.find("Adno").text
        course = self.sub_factories["courses"].get(Course(ids={"sims": course_id}, partial=True))
        student = self.sub_factories["students"].get(Student(ids={"admissionnumber": student_id}, partial=True))
        if course is None or student is None:
            return None
        m = md5()
        m.update((course.ids["sims"] + ':' + student.ids["sims"]).encode('utf-8'))
        item = {
            "ids": {"sims": m.hexdigest()},
            "details": {"student": student, "course": course},
        }
        return Enrolment(**item)
