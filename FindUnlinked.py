if __name__ == "__main__":
    from lib.questioner.Args import Args
    from lib.questioner.Combiner import Combiner
    from lib.questioner.File import File

    settings = Combiner(sources=[Args(), File()])

    from bin.Interface import build_interface
    from bin.Interface import get_requirements as get_interface_requirements

    interface = build_interface(
        settings.get("interface"),
        settings.get_many(get_interface_requirements(settings.get("interface"))),
    )

    from lib.questioner.Interface import Interface

    settings.add(Interface(interface))

    from bin.Connection import get_requirements as get_connection_requirements
    from bin.Connection import build_connection

    connection = build_connection(
        "Google",
        interface,
        settings.get("root_dir"),
        settings.get_many(get_connection_requirements("Google")),
    )

    from bin.Factory import get_requirements as get_factory_requirements
    from bin.Item import get_requirements as get_item_requirements

    factory = connection.build_factory(
        "User",
        settings.get_many(get_factory_requirements("Google", "User")),
        settings.get_many(get_item_requirements("User")),
    )

    from lib.item.User import User

    items = factory.list()
    for item in iter(items):
        user = User(**item)
        if "sims" not in user.ids:
            if user.ids["username"] not in (
                        "c.bloom",
                        "d.bull",
                        "r.emtage",
                        "b.hatton",
                        "t.jardine",
                        "g.lane",
                        "s.martin",
                        "j.riddell",
                        "r.saw",
                        "s.z-harvey",
                        "e.walsh",
                        "k.wigley",
                ) \
                    and (user.ids["username"][1] == "." or user.ids["username"][0].isdigit()):
                factory.delete(user)
                interface.put("DELETED: " + str(user))
            else:
                interface.put("KEPT:" + str(user))
