aliases = {
    "students": "Student",
    "view": "Interface", "here": "Interface",
}


def alias(name):
    return aliases.get(name, name[0].upper() + name[1:].lower())

