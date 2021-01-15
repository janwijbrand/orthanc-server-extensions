import logging
import re

import requests
from attr import dataclass

from orthanc_ext import event_dispatcher
from orthanc_ext.orthanc import OrthancApiHandler

orthanc = OrthancApiHandler()


@dataclass
class Event:
    change: orthanc.ChangeType = orthanc.ChangeType.UNKNOWN
    level: str = ""
    resource_id: str = ""


def capture(event):
    def capture_impl(incoming_event, orthanc):
        event.change = incoming_event.change_type
        event.resource_type = incoming_event.resource_type
        event.resource_id = incoming_event.resource_id

    return capture_impl


def test_registered_callback_should_be_triggered_on_change_event():
    event = Event()

    event_dispatcher.register_event_handlers({
        orthanc.ChangeType.ORTHANC_STARTED: capture(event)
    }, orthanc_module=orthanc)

    orthanc.on_change(orthanc.ChangeType.ORTHANC_STARTED, 'level', "resource-uuid")

    assert event.resource_id == "resource-uuid"
    assert event.level == 'level'


def test_no_registered_callbacks_should_be_reported_in_on_change_event(caplog):
    caplog.set_level(logging.INFO)

    event_dispatcher.register_event_handlers({}, orthanc_module=orthanc)
    orthanc.on_change(orthanc.ChangeType.ORTHANC_STARTED, 'level', "resource-uuid")

    assert "no handler registered for ORTHANC_STARTED" in caplog.text
