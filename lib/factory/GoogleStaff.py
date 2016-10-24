from lib.factory.GoogleUser import GoogleUser


class GoogleStaff(GoogleUser):

    @staticmethod
    def map(item):
        from lib.item.Staff import Staff
        output = GoogleUser.map(item)
        return Staff(**output) if "nihash" in output["ids"] else None
