from lib.factory.SimsBase import SimsBase


class SimsStaff(SimsBase):
    def __init__(self, connection, item_settings):
        try:
            super().__init__(connection, item_settings)
        except NotImplementedError:
            pass

    def list(self):
        return self.connection.list("staff")

    def map(self, item):
        from lib.item.Staff import Staff
        from _md5 import md5
        from lib.item.User import Helper
        output = super().map(item)
        if output.find("Prevent").text == "False" \
                and output.find("Surname").text is not None \
                and output.find("Forename").text is not None \
                and output.find("Surname").text[:1] != "$":
            m = md5()
            m.update(output.find("NI").text.encode("utf-8"))
            output = {
                "ids": {
                    "sims": output.find("primary_id").text,
                    "nihash": m.hexdigest(),
                },
                "details": {
                    "forename": Helper.abbreviate(output.find("Forename").text),
                    "surname": output.find("Surname").text,
                },
            }
        else:
            return None
        return Staff(**output)
