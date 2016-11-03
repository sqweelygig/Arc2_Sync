from lib.factory.GoogleBase import GoogleBase


class GoogleUser(GoogleBase):
    def __init__(self, connection, item_settings, domain):
        try:
            super().__init__(connection, item_settings)
        except NotImplementedError:
            pass
        self.domain = domain

    @staticmethod
    def get_requirements():
        return GoogleBase.get_requirements() | {"domain"}

    @staticmethod
    def get_common_arguments():
        return {
            "endpoint": "admin",
            "version": "directory_v1",
            "path": ["users"],
        }

    def get_list_arguments(self):
        return {
            **self.get_common_arguments(),
            "domain": self.domain,
            "key": "users",
        }

    def get_patch_arguments(self, item):
        return {
            **self.get_common_arguments(),
            "userKey": item.ids["username"] + "@" + self.domain,
            "body": self.unmap(item),
        }

    def get_delete_arguments(self, item):
        return {
            **self.get_common_arguments(),
            "userKey": item.ids["username"] + "@" + self.domain,
            "body": {
                "suspended": True,
            },
        }

    def get_put_arguments(self, item):
        # TODO Make this cope with suspended accounts?
        patch = self.unmap(item)
        # TODO something about username collisions, probably already half implemented in Student.py>Username
        username = item.get("username")
        patch["primaryEmail"] = username + "@" + self.domain
        item.ids["username"] = username
        patch["password"] = item.get("password")
        return {
            **self.get_common_arguments(),
            "body": patch,
        }

    def map(self, item):
        # TODO This should return User objects
        # from datetime import datetime
        # from datetime import timedelta
        item = super().map(item)
        output = {
            "ids": {
                "google": item["id"],
                "username": item["primaryEmail"].split("@")[0],
            },
            "details": {
                "forename": item["name"]["givenName"],
                "surname": item["name"]["familyName"],
                "username": item["primaryEmail"].split("@")[0],
                # "keep_until":
                #     datetime.strptime(item["lastLoginTime"], '%Y-%m-%dT%H:%M:%S.000Z')
                #     # TODO Put this into settings
                #     + timedelta(days=100),
            },
        }
        for external_id in item.get("externalIds", []):
            if external_id["customType"] is not "null":
                output["ids"][external_id["customType"].lower()] = external_id["value"]
        return output if not item["suspended"] else None

    def unmap(self, item):
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
