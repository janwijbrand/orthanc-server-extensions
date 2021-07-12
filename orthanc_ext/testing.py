# Testing infrastructure


class Capture:

    def __init__(self):
        self.events = []

    def __call__(self, event, client):
        self.events.append(event)
