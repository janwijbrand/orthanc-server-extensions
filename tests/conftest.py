import pytest

from orthanc_ext.event_dispatcher import Registry
from orthanc_ext.http_utilities import create_internal_client
from orthanc_ext.orthanc import OrthancApiHandler
from orthanc_ext.testing import Capture


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
    return Capture()
