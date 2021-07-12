from orthanc_ext.event_dispatcher import ChangeEvent


class Capture:

    def __init__(self) -> None:
        self.events: list[ChangeEvent] = []

    def __call__(self, event: ChangeEvent, client) -> None:
        self.events.append(event)
