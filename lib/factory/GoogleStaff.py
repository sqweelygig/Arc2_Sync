from lib.factory.GoogleUser import GoogleUser


class GoogleStaff(GoogleUser):
    def map(self, item):
        from lib.item.Staff import Staff
        item = super().map(item)
        return Staff(**item) if "nihash" in item["ids"] else None
