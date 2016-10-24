aliases = {
    "students": "Student",
    "view": "Text", "here": "Text",
    "courses": "Course",
}


def alias(name):
    return aliases.get(name, name[0].upper() + name[1:].lower())

