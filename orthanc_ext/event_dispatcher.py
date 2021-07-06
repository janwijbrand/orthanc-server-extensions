import dataclasses
import logging

from orthanc_ext.http_utilities import create_client
from orthanc_ext.orthanc import ChangeType, ResourceType

ANY = object()


@dataclasses.dataclass
class ChangeEvent:
    change_type: int
    resource_type: int
    resource_id: str

    def __str__(self):
        return (
            f'<{self.__class__.__name__} '
            f'change_type={ChangeType(self.change_type)} '
            f'resource_type={ResourceType(self.resource_type)} '
            f'resource_id={self.resource_id or None}>')


class Registry(dict):

    def __init__(self, orthanc, client=None):
        self._orthanc = orthanc
        self._client = client if client is not None else create_client(orthanc)

    def bind(self):
        self._orthanc.RegisterOnChangeCallback(self)

    def add_handler(self, event_type, *handlers):
        self.setdefault(event_type, []).extend(handlers)

    def unhandled_event(self, event, _):
        logging.debug(f'no handler registered for "{event}"')

    def handle_event(self, event):
        yield from (handler(event, self._client) for handler in self.get(ANY, []))
        yield from (
            handler(event, self._client)
            for handler in self.get(event.change_type, [self.unhandled_event]))

    def __call__(self, *params):
        return list(self.handle_event(ChangeEvent(*params)))


register_event_handlers = None
