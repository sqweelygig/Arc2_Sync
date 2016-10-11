from bin.Connection import Connection


class Sims(Connection):
    @staticmethod
    def get_requirements():
        return Connection.get_requirements() | {"username", "password"}

    def __init__(self, interface, root_dir, username, password):
        from os import path
        from os import makedirs
        try:
            super().__init__(interface, root_dir)
        except NotImplementedError:
            pass
        self.username = username
        self.password = password
        self.paths = {
            "data": path.join(self.root_dir, "data"),
            "definitions": path.join(self.root_dir, "definitions"),
        }
        for key, value in self.paths.items():
            if not path.exists(value):
                makedirs(value)

    def list(self, key, substitutions=None):
        from os import path
        from subprocess import run
        from xml.etree import ElementTree
        command = "C:" + path.sep + path.join("Program Files (x86)", "SIMS", "SIMS .net", "CommandReporter.exe")
        run([
            command,
            "/USER:" + self.username,
            "/PASSWORD:" + self.password,
            "/REPORT:arc2sync_" + key,
            "/OUTPUT:" + path.join(self.paths["definitions"], "arc2sync_" + key + ".xml"),
            "/PARAMDEF",
        ])
        if substitutions is not None:
            parameter_document = ElementTree.parse(path.join(self.paths["definitions"], "arc2sync_" + key + ".xml"))
            parameter_root = parameter_document.getroot()
            for parameter in parameter_root.findall("Parameter"):
                if parameter.attrib["id"] in substitutions:
                    parameter.set('bypass', 'FALSE')
                    for field in substitutions[parameter.attrib["id"]]:
                        parameter.find('Values').find(field).text = substitutions[parameter.attrib["id"]][field]
            parameter_document.write(path.join(self.paths["definitions"], "arc2sync_" + key + ".xml"))
        run([
            command,
            "/USER:" + self.username,
            "/PASSWORD:" + self.password,
            "/REPORT:arc2sync_" + key,
            "/OUTPUT:" + path.join(self.paths["data"], "arc2sync_" + key + ".xml"),
            "/PARAMFILE:" + path.join(self.paths["definitions"], "arc2sync_" + key + ".xml"),
        ])
        root = ElementTree.parse(path.join(self.paths["data"], "arc2sync_" + key + ".xml")).getroot()
        return root.findall("Record")
