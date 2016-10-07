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
        item_settings = settings.get_many(get_item_requirements(settings.get("sync")))
        source_settings = settings.get_many(get_connection_requirements(settings.get("from")))
        target_settings = settings.get_many(get_connection_requirements(settings.get("to")))
        settings.get("mode", '^(sync|fix|check|tweak)$')

        # Make connections


if __name__ == "__main__":
    print("## Building sync engine.")
    sync = Arc2Sync()
    print("## Pairing sync items.")
    # Pair[]
    # pairs = sync.pair();
    print("## Executing sync task.")
    # sync.execute(pairs);
    print("## Exiting sync app.")
