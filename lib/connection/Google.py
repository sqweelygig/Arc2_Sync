from bin.Connection import Connection


class Google(Connection):
    @staticmethod
    def get_requirements():
        return Connection.get_requirements() | {"domain"}

    def __init__(self, interface, domain):
        # TODO optimise imports
        from os import path
        from os import getenv
        from os import makedirs
        from _md5 import md5
        from oauth2client import file
        from oauth2client import client
        from oauth2client import tools
        from httplib2 import Http
        try:
            super().__init__(interface)
        except NotImplementedError:
            pass
        home_dir = path.join(getenv("APPDATA"), "Arc2Sync")
        credential_dir = path.join(home_dir, "credentials")
        if not path.exists(credential_dir):
            makedirs(credential_dir)
        m = md5()
        m.update(domain.encode("utf-8"))
        credential_path = path.join(credential_dir, m.hexdigest() + ".json")
        store = file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            scopes = (
                'https://www.googleapis.com/auth/admin.directory.user',
                'https://www.googleapis.com/auth/classroom.courses',
                'https://www.googleapis.com/auth/classroom.rosters'
            )
            secret = path.join("config", 'client_secret.json')
            name = 'Arc2 Sync'
            flow = client.flow_from_clientsecrets(secret, scopes)
            flow.user_agent = name
            credentials = tools.run_flow(flow, store)
        self.http = credentials.authorize(Http())
        self.domain = domain