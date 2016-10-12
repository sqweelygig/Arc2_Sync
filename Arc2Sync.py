class Arc2Sync:
    def __init__(self):
        # Get settings from command line arguments or default.py
        from lib.questioner.Args import Args
        from lib.questioner.Combiner import Combiner
        from lib.questioner.File import File
        self.settings = Combiner(sources=[Args(), File()])

        # Build the interface specified
        from bin.Interface import build_interface
        self.interface = build_interface(self.settings.get("interface"))

        # Add the interface as a source for settings
        self.settings.add(self.interface)

        # Pre-cache settings
        from bin.Item import get_requirements as get_item_requirements
        from bin.Connection import get_requirements as get_connection_requirements
        from bin.Factory import get_requirements as get_factory_requirements
        item_settings = self.settings.get_many(get_item_requirements(self.settings.get("sync")))
        source_settings = self.settings.get_many(get_connection_requirements(self.settings.get("from")))
        source_factory_settings = self.settings.get_many(
            get_factory_requirements(self.settings.get("from"), self.settings.get("sync"))
        )
        target_settings = self.settings.get_many(get_connection_requirements(self.settings.get("to")))
        target_factory_settings = self.settings.get_many(
            get_factory_requirements(self.settings.get("to"), self.settings.get("sync"))
        )
        self.settings.get("mode", '^(sync|fix|check|tweak)$')
        self.settings.get("root_dir")

        # Make connections
        from bin.Connection import build_connection
        from os import path
        from os import makedirs
        root_dir = self.settings.get("root_dir")
        if not path.exists(root_dir):
            makedirs(root_dir)
        connections = {
            self.settings.get("from"): build_connection(
                name=self.settings.get("from"),
                interface=self.interface,
                root_dir=root_dir,
                settings=source_settings,
            ),
            self.settings.get("to"): build_connection(
                name=self.settings.get("to"),
                interface=self.interface,
                root_dir=root_dir,
                settings=target_settings,
            ),
        }

        # Make factories
        factories = {
            self.settings.get("from"):
                connections
                .get(self.settings.get("from"))
                .build_factory(self.settings.get("sync"), source_factory_settings, item_settings),
            self.settings.get("to"):
                connections
                .get(self.settings.get("to"))
                .build_factory(self.settings.get("sync"), target_factory_settings, item_settings),
        }
        self.source_factory = factories.get(self.settings.get("from"))
        self.target_factory = factories.get(self.settings.get("to"))

    def gather(self):
        return {
            "source": self.source_factory.get(),
            "target": self.target_factory.get(),
        }

    def match(self, candidates):
        sections_to_do_keys = set()
        sections_done_keys = set()
        matches = []
        for section_to_do in iter(candidates):
            sections_to_do_keys.add(section_to_do)
        for section_focus, items in iter(candidates.items()):
            sections_to_do_keys.remove(section_focus)
            for item_focus in iter(items):
                match = {
                    section_focus: item_focus,
                }
                for section_done_key in iter(sections_done_keys):
                    match[section_done_key] = None
                for section_possible_key in iter(sections_to_do_keys):
                    match[section_possible_key] = None
                    for item_possible in iter(candidates[section_possible_key]):
                        if item_focus == item_possible:
                            match[section_possible_key] = item_possible
                            candidates[section_possible_key].remove(item_possible)
                            self.interface.reassure(str(item_focus) + ", " + str(item_possible))
                            break
                matches.append(match)
            sections_done_keys.add(section_focus)
        return matches

    def execute(self, matches):
        from datetime import datetime
        mode = self.settings.get("mode")

        do = mode not in {"check"}

        if mode in {"fix"}:
            for match in iter(matches):
                if match["target"] is None:
                    # ask, map match["source"]
                    pass

        if mode in {"check", "sync"}:
            for match in iter(matches):
                if match["source"] is None:
                    if match["target"].details.get("keep_until", None) is None or \
                                    match["target"].details.get("keep_until") < datetime.now():
                        self.interface.put("DELETE: " + str(match["target"]))
                        if do:
                            self.target_factory.delete(match["target"])

        if mode in {"check", "sync"}:
            for match in iter(matches):
                if match["target"] is None:
                    self.interface.put("CREATE: " + str(match["source"]))
                    if do:
                        self.target_factory.put(match["source"])

        if mode in {"check", "sync", "tweak", "fix"}:
            for match in iter(matches):
                if match["target"] is not None and match["source"] is not None:
                    if match["target"].enrich(match["source"]):
                        self.interface.put("UPDATE: " + str(match["source"]))
                        if do:
                            self.target_factory.patch(match["target"])


if __name__ == "__main__":
    print("## Building sync engine.")
    sync = Arc2Sync()
    print("## Gathering sync items.")
    responses = sync.gather()
    print("## Pairing sync items.")
    pairs = sync.match(responses)
    print("## Executing sync task.")
    sync.execute(pairs)
    print("## Exiting sync app.")
