from lib.factory.GoogleUser import GoogleUser


class GoogleStudent(GoogleUser):
    def map(self, item):
        from lib.item.Student import Student
        item = super().map(item)
        return Student(**item) if "admissionnumber" in item["ids"] else None

    def can_update(self, update):
        return super()._can_update(update, (), ("cohort",))
