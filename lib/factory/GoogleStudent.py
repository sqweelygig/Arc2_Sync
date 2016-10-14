from lib.factory.GoogleBase import GoogleBase


class GoogleStudent(GoogleBase):
    def __init__(self, connection, item_settings, domain):
        try:
            super().__init__(connection, item_settings)
        except NotImplementedError:
            pass
        self.domain = domain

    @staticmethod
    def get_requirements():
        return GoogleBase.get_requirements() | {"domain"}

    # TODO Combine common elements of below

    def get_list_arguments(self):
        return {
            "domain": self.domain,
            "endpoint": "admin",
            "version": "directory_v1",
            "path": ["users"],
            "key": "users",
        }

    def get_patch_arguments(self, item):
        return {
            "userKey": item.ids["username"] + "@" + self.domain,
            "endpoint": "admin",
            "version": "directory_v1",
            "path": ["users"]
        }

    def get_delete_arguments(self, item):
        return {
            "endpoint": "admin",
            "version": "directory_v1",
            "path": ["users"],
            "userKey": item.ids["username"] + "@" + self.domain,
        }

    @staticmethod
    def map(item):
        from datetime import datetime
        from datetime import timedelta
        from lib.item.Student import Student
        output = GoogleBase.map(item)
        output = {
            "ids": {
                "google": output["id"],
                "username": output["primaryEmail"].split("@")[0],
            },
            "details": {
                "forename": output["name"]["givenName"],
                "surname": output["name"]["familyName"],
                "username": output["primaryEmail"].split("@")[0],
                "keep_until":
                    datetime.strptime(output["lastLoginTime"], '%Y-%m-%dT%H:%M:%S.000Z')
                    # TODO Put this into settings
                    + timedelta(days=100)
                ,
            },
        }
        for external_id in item.get("externalIds", []):
            if external_id["customType"] is not "null":
                output["ids"][external_id["customType"].lower()] = external_id["value"]
        return Student(**output) if "admissionnumber" in output["ids"] else None

    @staticmethod
    def unmap(item, purpose=None):
        output = {
            "externalIds": [],
            "name": {"givenName": item.details["forename"], "familyName": item.details["surname"]}
        }
        for external_id in item.ids:
            output["externalIds"].append({
                "type": "custom",
                "customType": external_id,
                "value": item.ids[external_id]
            })
        return output
