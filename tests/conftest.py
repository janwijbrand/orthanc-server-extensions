from attr import s
import pytest

from orthanc_ext.event_dispatcher import Registry
from orthanc_ext.http_utilities import create_internal_client
from orthanc_ext.orthanc import OrthancApiHandler


@pytest.fixture
def orthanc():
    return OrthancApiHandler()


@pytest.fixture
def registry(orthanc):
    registry = Registry(
        orthanc,
        create_internal_client(
            base_url='https://localhost:8042', token=orthanc.GenerateRestApiAuthorizationToken()))
    registry.bind()
    return registry


@pytest.fixture
def capture():

    class Capture:

        def __init__(self):
            self.events = []

        def __call__(self, event, client):
            self.events.append(event)

    return Capture()
