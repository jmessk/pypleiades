import logging.config
import pytest
import logging

from pymec.api import data_api


SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def input_data():
    return b"Hello, World!"


def test_post_data(input_data):
    response = data_api.post_data(SERVER_URL, input_data).unwrap()
    assert response.code == 0
