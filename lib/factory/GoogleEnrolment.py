from lib.factory.GoogleBase import GoogleBase
from lib.factory.GoogleCourse import GoogleCourse
from lib.factory.GoogleStudent import GoogleStudent


class GoogleEnrolment(GoogleBase):
    def get_list_arguments(self):
        raise NotImplementedError

    def get_delete_arguments(self, item):
        raise NotImplementedError

    def get_patch_arguments(self, item):
        raise NotImplementedError

    def get_put_arguments(self, item):
        item.details["course"].enrich(self.sub_factories["courses"].get(item.details["course"]))
        item.details["student"].enrich(self.sub_factories["students"].get(item.details["student"]))
        return {
            **self.get_common_arguments(),
            "courseId": item.details["course"].ids["google"],
            "body": {
                "courseId": item.details["course"].ids["google"],
                "userId": item.details["student"].ids["google"],
            }
        }

    def __init__(self, connection, interface, item_settings, domain):
        try:
            super().__init__(connection, interface, item_settings)
        except NotImplementedError:
            pass
        self.sub_factories = {
            "courses": GoogleCourse(connection, interface, {}, domain),
            "students": GoogleStudent(connection, interface, {}, domain),
        }

    @staticmethod
    def get_common_arguments():
        return {
            "endpoint": "classroom",
            "version": "v1",
            "path": ["courses", "students"],
        }

    def fetch(self):
        output = []
        courses = self.sub_factories["courses"].list()
        for course in courses:
            for student in self.connection.list(
                    **self.get_common_arguments(),
                    courseId=course.ids["google"],
                    key="students",
            ):
                output.append(student)
        return output

    def map(self, item):
        from lib.item.Course import Course
        from lib.item.Student import Student
        from lib.item.Enrolment import Enrolment
        from _md5 import md5
        course = self.sub_factories["courses"].get(Course(ids={"google": item["courseId"]}, partial=True))
        student = self.sub_factories["students"].get(Student(ids={"google": item["userId"]}, partial=True))
        if course is None or student is None:
            return None
        sims_id = md5()
        sims_id.update((course.ids["sims"] + ':' + student.ids["sims"]).encode('utf-8'))
        sims_id = sims_id.hexdigest()
        google_id = md5()
        google_id.update((course.ids["google"] + ':' + course.ids["google"]).encode('utf-8'))
        google_id = google_id.hexdigest()
        item = {
            "ids": {
                "sims": sims_id,
                "google": google_id,
            },
            "details": {
                "student": student,
                "course": course,
            },
        }
        return Enrolment(**item)

    @staticmethod
    def get_requirements():
        return GoogleCourse.get_requirements() | GoogleStudent.get_requirements()
