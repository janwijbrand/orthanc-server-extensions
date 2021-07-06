"""Test entry point script for Orthanc Python Plugin.
"""

import logging

import orthanc as runtime  # NOQA provided by the plugin runtime.

from orthanc_ext import event_dispatcher
from orthanc_ext import orthanc
from orthanc_ext.logging_configurator import orthanc_logging


orthanc_logging(runtime)


def log_event(event, _):
    logging.info(f'orthanc "{event}" handled')


def start_maintenance_cycle(event, _):
    logging.info(f'Orthanc start maintenance cycle')


def show_system_info(_, client):
    version = client.get('/system').json().get('Version')
    logging.warning(f'Orthanc version "{version}"', )


def stop_handler(event, _):
    logging.info(f'Orthanc stop handler')


registry = event_dispatcher.Registry(runtime)
registry.add_handler(event_dispatcher.ANY, log_event)
registry.add_handler(
    runtime.ChangeType.ORTHANC_STARTED,
    start_maintenance_cycle, show_system_info)
registry.add_handler(
    runtime.ChangeType.ORTHANC_STOPPED,
    stop_handler)
registry.bind()
