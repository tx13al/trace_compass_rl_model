class Action:
    def __init__(self, event_type):
        self.event_type = event_type

    def __str__(self):
        return self.event_type

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)
