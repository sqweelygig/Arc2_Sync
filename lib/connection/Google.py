from bin.Connection import Connection


class Google(Connection):
    @staticmethod
    def get_requirements():
        return Connection.get_requirements() | {"domain"}

    def __init__(self, interface, root_dir, domain):
        # TODO optimise imports
        from os import path
        from os import makedirs
        from _md5 import md5
        from oauth2client import file
        from oauth2client import client
        from oauth2client import tools
        from httplib2 import Http
        try:
            super().__init__(interface, root_dir)
        except NotImplementedError:
            pass
        credential_dir = path.join(self.root_dir, "credentials")
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

    def get_service(self, endpoint, version, path):
        from googleapiclient import discovery
        service = discovery.build(endpoint, version, http=self.http)
        for node in path:
            service = getattr(service, node)()
        return service

    def patch(self, endpoint, version, path, **kwargs):
        self.get_service(endpoint, version, path).patch(**kwargs).execute()

    # def delete(self, endpoint, version, path, **kwargs):
        # self.get_service(endpoint, version, path).delete(**kwargs).execute()

    def insert(self, endpoint, version, path, **kwargs):
        self.get_service(endpoint, version, path).insert(**kwargs).execute()

    def list(self, endpoint, version, path, key, **kwargs):
        from functools import partial
        task = partial(self.get_service(endpoint, version, path).list, **kwargs)

        # Iterate around the pages that list gives
        output = []
        next_page = True
        pages = 1
        while bool(next_page):
            response = task().execute() if next_page is True else task(pageToken=next_page).execute()
            next_page = response.get("nextPageToken", False)
            self.interface.reassure("Found " + str(pages) + " page(s) of " + key)
            pages += 1
            output += response.get(key, [])

        return output
