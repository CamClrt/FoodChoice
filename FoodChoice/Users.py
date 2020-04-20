class Users:

    def __init__(self, name, pwd, substitutes, id=None):
        self.id = id
        self.name = name
        self.pwd = pwd
        self.substitutes = substitutes

    def __repr__(self):
        return f"{self.name}, {self.pwd}, {self.substitutes}"

    def display_as_tuple(self):
        return (self.name, self.pwd, self.substitutes)