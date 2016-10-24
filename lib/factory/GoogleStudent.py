from lib.factory.GoogleUser import GoogleUser


class GoogleStudent(GoogleUser):
    @staticmethod
    def map(item):
        from lib.item.Student import Student
        output = GoogleUser.map(item)
        return Student(**output) if "admissionnumber" in output["ids"] else None
