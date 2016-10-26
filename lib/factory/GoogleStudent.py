from lib.factory.GoogleUser import GoogleUser


class GoogleStudent(GoogleUser):
    def map(self, item):
        from lib.item.Student import Student
        output = super().map(item)
        return Student(**output) if "admissionnumber" in output["ids"] else None
