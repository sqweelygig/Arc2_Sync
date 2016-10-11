from lib.factory.SimsBase import SimsBase


class SimsStudent(SimsBase):
    def __init__(self, connection, item_settings):
        try:
            super().__init__(connection, item_settings)
        except NotImplementedError:
            pass

    def list(self):
        return self.connection.list("students")

    @staticmethod
    def map(item):
        from lib.item.Student import Student
        from datetime import datetime
        output = SimsBase.map(item)
        if output.find("Prevent_x0020_IT_x0020_sync_x003F_").text == "False"\
                and output.find("Preferred_x0020_Surname").text is not None \
                and output.find("Preferred_x0020_Forename").text is not None \
                and output.find("DOB").text is not None \
                and output.find("Preferred_x0020_Surname").text[:1] != "$":
            dob = datetime.strptime(output.find("DOB").text[0:10], '%Y-%m-%d')
            if dob.month > 8:
                intake_after_dob = dob.year + 1
            else:
                intake_after_dob = dob.year
            cohort = (intake_after_dob + 11) % 1000
            output = {
                "ids": {
                    "sims": output.find("primary_id").text,
                    "admissionnumber": output.find("Adno").text,
                },
                "details": {
                    "forename": output.find("Preferred_x0020_Forename").text,
                    "surname": output.find("Preferred_x0020_Surname").text,
                    "cohort": cohort,
                },
            }
        else:
            return None
        return Student(**output)
