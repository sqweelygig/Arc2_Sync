from lib.factory.GoogleBase import GoogleBase
from lib.factory.GoogleCourse import GoogleCourse
from lib.factory.GoogleStaff import GoogleStaff


class GoogleSupervisor(GoogleBase):
    def populate_ids(self, item):
        if "google" not in item.details["course"].ids:
            item.details["course"].enrich(self.sub_factories["courses"].get(item.details["course"]))
        if "google" not in item.details["supervisor"].ids:
            item.details["supervisor"].enrich(self.sub_factories["staff"].get(item.details["supervisor"]))

    def get_list_arguments(self):
        # Uses non-standard fetch function
        raise NotImplementedError

    def get_delete_arguments(self, item):
        # Not yet implemented
        raise NotImplementedError

    def get_patch_arguments(self, item):
        # Nothing may be updated
        raise NotImplementedError

    def get_put_arguments(self, item):
        self.populate_ids(item)
        return {
            **self.get_common_arguments(),
            "courseId": item.details["course"].ids["google"],
            "body": {
                "courseId": item.details["course"].ids["google"],
                "userId": item.details["supervisor"].ids["google"],
            }
        }

    def __init__(self, connection, interface, item_settings, domain):
        try:
            super().__init__(connection, interface, item_settings)
        except NotImplementedError:
            pass
        self.sub_factories = {
            "courses": GoogleCourse(connection, interface, {}, domain),
            "staff": GoogleStaff(connection, interface, {}, domain),
        }

    @staticmethod
    def get_common_arguments():
        return {
            "endpoint": "classroom",
            "version": "v1",
            "path": ["courses", "teachers"],
        }

    def fetch(self):
        output = []
        courses = self.sub_factories["courses"].list()
        for course in courses:
            if "teacher" in course.details and course.details["teacher"] is not None:
                output.append({
                    "courseId": course.ids["google"],
                    "userId": course.details["teacher"].ids["google"]
                })
            for teacher in self.connection.list(
                    **self.get_common_arguments(),
                    courseId=course.ids["google"],
                    key="teachers",
            ):
                output.append(teacher)
        return output

    def map(self, item):
        from lib.item.Course import Course
        from lib.item.Staff import Staff
        from lib.item.Enrolment import Enrolment
        from _md5 import md5
        course = self.sub_factories["courses"].get(Course(ids={"google": item["courseId"]}, partial=True))
        supervisor = self.sub_factories["staff"].get(Staff(ids={"google": item["userId"]}, partial=True))
        if course is None or supervisor is None:
            return None
        sims_id = md5()
        sims_id.update((course.ids["sims"] + ':' + supervisor.ids["sims"]).encode('utf-8'))
        sims_id = sims_id.hexdigest()
        google_id = md5()
        google_id.update((course.ids["google"] + ':' + supervisor.ids["google"]).encode('utf-8'))
        google_id = google_id.hexdigest()
        item = {
            "ids": {
                "sims": sims_id,
                "google": google_id,
            },
            "details": {
                "supervisor": supervisor,
                "course": course,
            },
        }
        return Enrolment(**item)

    @staticmethod
    def get_requirements():
        return GoogleCourse.get_requirements() | GoogleStaff.get_requirements()
