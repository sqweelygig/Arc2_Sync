class Arc2Sync:
    def __init__(self):
        # Get settings from command line arguments or default.py
        from lib.questioner.Args import Args
        from lib.questioner.Combiner import Combiner
        from lib.questioner.File import File
        settings = Combiner(sources=[Args(), File()])

        # Build the interface specified
        from bin.Interface import build_interface
        self.interface = build_interface(settings.get("interface"))

        # Add the interface as a source for settings
        settings.add(self.interface)

        # Pre-cache settings
        from bin.Item import get_requirements as get_item_requirements
        from bin.Connection import get_requirements as get_connection_requirements
        from bin.Factory import get_requirements as get_factory_requirements
        item_settings = settings.get_many(get_item_requirements(settings.get("sync")))
        source_settings = settings.get_many(get_connection_requirements(settings.get("from")))
        source_factory_settings = settings.get_many(
            get_factory_requirements(settings.get("from"), settings.get("sync"))
        )
        target_settings = settings.get_many(get_connection_requirements(settings.get("to")))
        target_factory_settings = settings.get_many(
            get_factory_requirements(settings.get("to"), settings.get("sync"))
        )
        settings.get("mode", '^(sync|fix|check|tweak)$')
        settings.get("root_dir")

        # Make connections
        from bin.Connection import build_connection
        from os import path
        from os import makedirs
        root_dir = settings.get("root_dir")
        if not path.exists(root_dir):
            makedirs(root_dir)
        connections = {
            settings.get("from"): build_connection(
                name=settings.get("from"),
                interface=self.interface,
                root_dir=root_dir,
                settings=source_settings,
            ),
            settings.get("to"): build_connection(
                name=settings.get("to"),
                interface=self.interface,
                root_dir=root_dir,
                settings=target_settings,
            ),
        }

        # Make factories
        factories = {
            settings.get("from"):
                connections
                .get(settings.get("from"))
                .build_factory(settings.get("sync"), source_factory_settings, item_settings),
            settings.get("to"):
                connections
                .get(settings.get("to"))
                .build_factory(settings.get("sync"), target_factory_settings, item_settings),
        }
        self.source_factory = factories.get(settings.get("from"))
        self.target_factory = factories.get(settings.get("to"))

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
                self.interface.reassure(item_focus)
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
                            break
                matches.append(match)
            sections_done_keys.add(section_focus)
        return matches

    def execute(self, matches):
        for match in matches:
            self.interface.reassure(str(match["source"]) + ", " + str(match["target"]))


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
