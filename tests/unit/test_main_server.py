import os, sys
import tempfile

import pytest

from server.models import RaspberryPi

def test_new_rpi():
    """
    GIVEN a RaspberryPi model
    WHEN a new RaspberryPi is created
    THEN check ip_address, name fields are defined correctly
    """
    new_rpi = RaspberryPi(name="entry", ip_address="192.168.0.2")
    assert new_rpi.name == "entry"
    assert new_rpi.ip_address == "192.168.0.2"

def test_register_new_rpi():
    pass

def test_register_already_registered_rpi():
    pass

def test_register_modify_ip_of_already_registered_rpi():
    pass


