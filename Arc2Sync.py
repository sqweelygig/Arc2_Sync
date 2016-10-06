from importlib import import_module

from lib.questioner.Interface import Interface
from lib.questioner.Args import Args
from lib.questioner.Combiner import Combiner
from lib.questioner.File import File
from aliases import alias


class Arc2Sync:
    def __init__(self):
        # Get settings from command line arguments or default.py
        settings = Combiner(sources=[Args(), File()])

        # Build the interface specified
        interface = get_class("interface", settings.get("interface"))()

        # Add the interface as a source for settings
        settings.add(source=Interface(interface))

        # Pre-cache settings
        settings.get("sync")
        source_settings = settings.get_many(get_requirements("endpoint", settings.get("from")))
        target_settings = settings.get_many(get_requirements("endpoint", settings.get("to")))
        settings.get("mode", '^(sync|fix|check|tweak)$')

        # Connect to endpoints
        self.source = get_class("endpoint", settings.get("from"))(interface=interface, **source_settings)
        self.target = get_class("endpoint", settings.get("to"))(interface=interface, **target_settings)


def get_class(model, name):
    name = alias(name)
    return getattr(
        import_module("lib." + model.lower() + "." + name[0].upper() + name[1:].lower()),
        name[0].upper() + name[1:].lower()
    )


def get_requirements(model, name):
    name = alias(name)
    module = import_module("lib." + model.lower() + "." + name[0].upper() + name[1:].lower())
    return getattr(module, "requirements") if hasattr(module, "requirements") else ()


if __name__ == "__main__":
    print("## Building sync engine.")
    sync = Arc2Sync()
    print("## Pairing sync items.")
    # Pair[]
    # pairs = sync.pair();
    print("## Executing sync task.")
    # sync.execute(pairs);
    print("## Exiting sync app.")
