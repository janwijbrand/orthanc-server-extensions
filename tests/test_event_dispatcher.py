import logging

import respx
from orthanc_ext.event_dispatcher import ChangeEvent, Registry
from orthanc_ext.logging_configurator import python_logging
from orthanc_ext.orthanc import OrthancApiHandler, ChangeType, ResourceType


def test_registered_callback_should_be_triggered_on_change_event(orthanc, registry, capture):
    registry.add_handler(ChangeType.STABLE_STUDY, capture)
    orthanc.on_change(ChangeType.STABLE_STUDY, ResourceType.STUDY, 'resource-uuid')
    assert len(capture.events) == 1

    event = capture.events[0]
    assert event.resource_id == 'resource-uuid'
    assert event.resource_type == ResourceType.STUDY


def test_all_registered_callbacks_should_be_triggered_on_change_event(orthanc, registry, capture):
    registry.add_handler(ChangeType.STABLE_STUDY, capture)
    registry.add_handler(ChangeType.STABLE_STUDY, capture)
    orthanc.on_change(ChangeType.STABLE_STUDY, ResourceType.STUDY, 'resource-uuid')
    assert len(capture.events) == 2

    event0, event1 = capture.events
    assert event0.resource_id == 'resource-uuid'
    assert event0.resource_type == ResourceType.STUDY
    assert event1.resource_id == 'resource-uuid'
    assert event1.resource_type == ResourceType.STUDY


# def test_no_registered_callbacks_should_be_reported_in_on_change_event(caplog):
#     args = {}
#     event_dispatcher.register_event_handlers(
#         args, orthanc, httpx, logging_configuration=python_logging)
#     caplog.set_level(logging.DEBUG)
#     orthanc.on_change(orthanc.ChangeType.ORTHANC_STARTED, '', '')
#     assert 'no handler registered for ORTHANC_STARTED' in caplog.text


@respx.mock
def test_shall_return_values_from_executed_handlers(orthanc, registry):
    system = respx.get('/system').respond(200, json={'Version': '1.9.0'})

    def get_system_info(event, client):
        return client.get('http://localhost:8042/system').json()

    registry.add_handler(ChangeType.ORTHANC_STARTED, get_system_info)
    (system_info, ) = orthanc.on_change(
        ChangeType.ORTHANC_STARTED, ResourceType.NONE, 'resource-uuid')
    assert system.called
    assert system_info.get('Version') == '1.9.0'


# def test_event_shall_have_human_readable_representation(caplog):
#     caplog.set_level(logging.INFO)

#     def log_event(evt, _):
#         logging.info(evt)

#     event_dispatcher.register_event_handlers(
#         {orthanc.ChangeType.STABLE_STUDY: log_event}, orthanc, httpx)
#     orthanc.on_change(orthanc.ChangeType.STABLE_STUDY, orthanc.ResourceType.STUDY, 'uuid')
#     assert 'change_type=STABLE_STUDY' in caplog.text
#     assert 'resource_type=STUDY' in caplog.text
