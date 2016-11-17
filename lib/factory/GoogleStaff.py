from lib.factory.GoogleUser import GoogleUser


class GoogleStaff(GoogleUser):
    def map(self, item):
        from lib.item.Staff import Staff
        item = super().map(item)
        return Staff(**item) if item is not None and "ids" in item and "nihash" in item["ids"] else None
