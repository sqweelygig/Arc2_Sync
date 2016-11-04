from lib.factory.SimsBase import SimsBase


class SimsStudent(SimsBase):
    def __init__(self, connection, interface, item_settings):
        try:
            super().__init__(connection, interface, item_settings)
        except NotImplementedError:
            pass

    def fetch(self):
        return self.connection.list("students")

    def map(self, item):
        from lib.item.Student import Student
        from datetime import datetime
        item = super().map(item)
        if item.find("Prevent").text == "False"\
                and item.find("Surname").text is not None \
                and item.find("Forename").text is not None \
                and item.find("DOB").text is not None \
                and item.find("Surname").text[:1] != "$":
            dob = datetime.strptime(item.find("DOB").text[0:10], '%Y-%m-%d')
            if dob.month > 8:
                intake_after_dob = dob.year + 1
            else:
                intake_after_dob = dob.year
            cohort = (intake_after_dob + 11) % 1000
            item = {
                "ids": {
                    "sims": item.find("primary_id").text,
                    "admissionnumber": item.find("Adno").text,
                },
                "details": {
                    "forename": item.find("Forename").text,
                    "surname": item.find("Surname").text,
                    "cohort": cohort,
                },
            }
        else:
            return None
        return Student(**item)
