from importlib import import_module

from lib.questioner.Interface import Interface
from lib.questioner.Args import Args
from lib.questioner.Combiner import Combiner
from lib.questioner.File import File


class Arc2Sync:
    def __init__(self):
        # Get settings from command line arguments or default.py
        settings = Combiner(sources=[Args(), File()])

        # Build the interface specified
        interface = self.get("interface", settings.get("interface"))()

        # Add the interface as a source for settings
        settings.add(source=Interface(interface))

        # Get the standard settings
        settings.get("sync")
        settings.get("from")
        settings.get("to")
        settings.get("mode", '^(sync|fix|check|tweak)$')

    @staticmethod
    def get(model, name):
        return getattr(
            import_module("lib." + model.lower() + "." + name[0].upper() + name[1:].lower()),
            name[0].upper() + name[1:].lower()
        )


if __name__ == "__main__":
    print("## Building sync engine.")
    sync = Arc2Sync()
    print("## Pairing sync items.")
    # Pair[]
    # pairs = sync.pair();
    print("## Executing sync task.")
    # sync.execute(pairs);
    print("## Exiting sync app.")
