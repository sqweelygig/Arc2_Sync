aliases = {
    "students": "student",
    "view": "interface", "here": "interface",
}


def alias(name):
    return aliases.get(name, name)

