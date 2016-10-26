from lib.factory.GoogleUser import GoogleUser


class GoogleStaff(GoogleUser):
    def map(self, item):
        from lib.item.Staff import Staff
        output = super().map(item)
        return Staff(**output) if "nihash" in output["ids"] else None
