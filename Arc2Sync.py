class Arc2Sync:
    def __init__(self):
        # Get settings from command line arguments or default.py
        from lib.questioner.Args import Args
        from lib.questioner.Combiner import Combiner
        from lib.questioner.File import File
        settings = Combiner(sources=[Args(), File()])

        # Build the interface specified
        from bin.Interface import build_interface
        interface = build_interface(settings.get("interface"))

        # Add the interface as a source for settings
        settings.add(interface)

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

        # Make connections
        from bin.Connection import build_connection
        connections = {
            settings.get("from"): build_connection(
                name=settings.get("from"),
                interface=interface,
                settings=source_settings,
            ),
            settings.get("to"): build_connection(
                name=settings.get("to"),
                interface=interface,
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


if __name__ == "__main__":
    print("## Building sync engine.")
    sync = Arc2Sync()
    print("## Pairing sync items.")
    # Pair[]
    # pairs = sync.pair();
    print("## Executing sync task.")
    # sync.execute(pairs);
    print("## Exiting sync app.")
