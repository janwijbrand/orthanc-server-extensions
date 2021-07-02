import dataclasses
import json
import logging

from orthanc_ext.http_utilities import (
    create_internal_client, get_certificate, get_rest_api_base_url)
from orthanc_ext.logging_configurator import orthanc_logging
from orthanc_ext.python_utilities import create_reverse_type_dict, ensure_iterable


def register_event_handler(event, handler, module, client, logging_configuration=orthanc_logging):
    pass


def register_event_handlers(
        event_handlers, orthanc_module, client, logging_configuration=orthanc_logging):
    logging_configuration(orthanc_module)

    @dataclasses.dataclass
    class ChangeEvent:
        change_type: int
        resource_type: int
        resource_id: str

        def __str__(self):
            return (
                f'ChangeEvent(change_type={event_types.get(self.change_type)}, '
                f'resource_type={resource_types.get(self.resource_type)}, '
                f'resource_id="{self.resource_id}")')

    def create_type_index(orthanc_type):
        return create_reverse_type_dict(orthanc_type)

    event_types = create_type_index(orthanc_module.ChangeType)
    resource_types = create_type_index(orthanc_module.ResourceType)
    event_handlers = {k: ensure_iterable(v) for k, v in event_handlers.items()}

    def unhandled_event_logger(event, _):
        logging.debug(f'no handler registered for {event_types[event.change_type]}')

    def OnChange(change_type, resource_type, resource_id):
        handlers = event_handlers.get(change_type, [unhandled_event_logger])
        return_values = []
        for handler in handlers:
            event = ChangeEvent(change_type, resource_type, resource_id)
            return_values.append(handler(event, client))
        return return_values

    orthanc_module.RegisterOnChangeCallback(OnChange)


def create_client(orthanc):
    config = json.loads(orthanc.GetConfiguration())
    return create_internal_client(
        get_rest_api_base_url(config), orthanc.GenerateRestApiAuthorizationToken(),
        get_certificate(config))
