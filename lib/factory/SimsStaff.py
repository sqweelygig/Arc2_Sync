from lib.factory.SimsBase import SimsBase


class SimsStaff(SimsBase):
    def __init__(self, connection, interface, item_settings):
        try:
            super().__init__(connection, interface, item_settings)
        except NotImplementedError:
            pass

    def fetch(self):
        return self.connection.list("staff")

    def map(self, item):
        from lib.item.Staff import Staff
        from _md5 import md5
        from lib.item.User import Helper
        item = super().map(item)
        if item.find("Prevent").text == "False" \
                and item.find("Surname").text is not None \
                and item.find("Forename").text is not None \
                and item.find("Surname").text[:1] != "$":
            m = md5()
            m.update(item.find("NI").text.encode("utf-8"))
            output = {
                "ids": {
                    "sims": item.find("primary_id").text,
                    "nihash": m.hexdigest(),
                },
                "details": {
                    "forename": Helper.abbreviate(item.find("Forename").text),
                    "surname": item.find("Surname").text,
                },
            }
        else:
            return None
        return Staff(**output)
