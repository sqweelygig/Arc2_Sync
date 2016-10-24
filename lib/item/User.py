from bin.Item import Item


class User(Item):
    def __init__(self, ids, details):
        try:
            super().__init__(ids, details)
        except NotImplementedError:
            pass

    @staticmethod
    def get_core_fields():
        output = Item.get_core_fields()
        output.add("forename")
        output.add("surname")
        return output

    @staticmethod
    def suggest_password():
        return Password.readable()

    def suggest_username(self):
        return Username(self.details).__next__()


class Password:
    @staticmethod
    def readable(length=8, seed=None):
        from random import randint
        from random import seed as seed_random
        from importlib import import_module
        sounds = (
            ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'x', 'z', 'ch', 'gh', 'sh',
             'th'),
            ('a', 'e', 'u', 'y', 'ee', 'ue', 'ae', 'ea')
        )
        naughty = import_module("config.Default").swearwords
        seed_random(seed)
        output = ""
        while output == "":
            bank = randint(0, 1)
            while len(output) < length - 1:
                append = sounds[bank][randint(0, len(sounds[bank]) - 1)]
                if len(output + append) <= length - 1:
                    bank = not bank
                    output += append
            while len(output) < length:
                output += (str(randint(2, 9)))
            for word in iter(naughty):
                if word in output:
                    output = ""
        return output


class Username:
    def __init__(self, details):
        self.index = 0
        self.suggestions = []
        if details != {}:
            self.suggestions += Username.cohort_initial_dot_surname(details)
            self.suggestions += Username.cohort_forename_dot_surname(details)
            self.suggestions += Username.cohort_initial_or_forename_dot_surname_shorten(details)
            self.suggestions += Username.cohort_initial_dot_surname_shorten(details)
            self.suggestions = list(filter(lambda x: len(x) <= 13, self.suggestions))
            self.final = list(filter(lambda x: len(x) <= 12, self.suggestions))[0]
        else:
            self.final = ""

    @staticmethod
    def combine_parts(parts):
        from re import sub
        return sub(r'\s+', '_', "".join(parts).lower())

    @staticmethod
    def cohort_initial_dot_surname(details):
        username_parts = []
        if "cohort" in details:
            username_parts.append(str(details["cohort"]))
        username_parts.append(details["forename"][0])
        username_parts.append(".")
        username_parts.append(details["surname"])
        return [Username.combine_parts(username_parts)]

    @staticmethod
    def cohort_forename_dot_surname(details):
        username_parts = []
        if "cohort" in details:
            username_parts.append(str(details["cohort"]))
        username_parts.append(Helper.split(details["forename"])[0])
        username_parts.append(".")
        username_parts.append(details["surname"])
        return [Username.combine_parts(username_parts)]

    @staticmethod
    def cohort_initial_or_forename_dot_surname_shorten(details):
        usernames = []
        surname_parts = Helper.split(details["surname"], ())
        for i in range(0, len(surname_parts)):
            username_parts = []
            if "cohort" in details:
                username_parts.append(str(details["cohort"]))
            if i == len(surname_parts) - 1:
                username_parts.append(Helper.split(details["forename"])[0])
            else:
                username_parts.append(details["forename"][0])
            username_parts.append(".")
            if surname_parts[i].strip() != "":
                surname_parts[i] = surname_parts[i].strip()[0]
            else:
                surname_parts[i] = surname_parts[i].strip()
            username_parts.append("".join(surname_parts))
            usernames.append(Username.combine_parts(username_parts))
        output = []
        for username in usernames:
            if username not in output:
                output.append(username)
        return output

    @staticmethod
    def cohort_initial_dot_surname_shorten(details):
        username_parts = []
        if "cohort" in details:
            username_parts.append(str(details["cohort"]))
        username_parts.append(details["forename"][0].lower())
        username_parts.append(".")
        surname_parts = []
        for part in Helper.split(details["surname"], ()):
            if part.strip() != "":
                surname_parts.append(part.strip()[0].lower())
            else:
                surname_parts.append(part.strip())
        username_parts.append("".join(surname_parts))
        return [Username.combine_parts(username_parts)]

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.suggestions):
            output = self.suggestions[self.index]
        else:
            output = self.final + str(self.index - len(self.suggestions))
        self.index += 1
        return output


class Helper:
    @staticmethod
    def split(value, special=("mac", "mc")):
        output = []
        buffer = None
        last = None
        for character in value:
            if last is None:
                buffer = character
                last = character.isalnum()
            elif buffer.lower() in special:
                output.append(buffer)
                buffer = character
                last = character.isalnum()
            elif character.isalnum() == last:
                buffer += character
            else:
                output.append(buffer)
                buffer = character
                last = character.isalnum()
        output.append(buffer)
        return output

    @staticmethod
    def upper_first(value):
        return value[:1].upper() + value[1:].lower()

    @staticmethod
    def abbreviate(value, target=0):
        array_new = Helper.split(value)

        array_old = array_new
        array_new = []
        for word in array_old:
            if len(word.strip()) == 0:
                array_new.append(" ")
            else:
                array_new.append(word.strip())
        index = 0
        while len("".join(array_new)) > target and index < len(array_new):
            array_new[index] = array_new[index][0]
            index += 1
        return "".join(array_new)
