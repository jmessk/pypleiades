import pytest
import logging.config
import logging

from pymec.api import data_api


SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


@pytest.fixture
def input_bytes():
    return b"Hello, World!"


def test_post_data(input_bytes):
    response_post = data_api.post_data(SERVER_URL, input_bytes).unwrap()

    assert response_post.code == 0
    assert response_post.data_id != "0"
    assert response_post.data_id != ""


@pytest.mark.asyncio
async def test_post_data_async(input_bytes):
    response_post = (await data_api.post_data_async(SERVER_URL, input_bytes)).unwrap()

    assert response_post.code == 0
    assert response_post.data_id != "0"
    assert response_post.data_id != ""


def test_get_data(input_bytes):
    response_post = data_api.post_data(SERVER_URL, input_bytes).unwrap()
    response_get = data_api.get_data(SERVER_URL, response_post.data_id).unwrap()

    assert response_get == input_bytes


@pytest.mark.asyncio
async def test_get_data_async(input_bytes):
    response_post = (await data_api.post_data_async(SERVER_URL, input_bytes)).unwrap()
    response_get = (
        await data_api.get_data_async(SERVER_URL, response_post.data_id)
    ).unwrap()

    assert response_get == input_bytes


def test_info(input_bytes):
    response_post = data_api.post_data(SERVER_URL, input_bytes).unwrap()
    response_info = data_api.info(SERVER_URL, response_post.data_id).unwrap()

    assert response_info.code == 0
    assert response_info.data_id != "0"
    assert response_info.data_id != ""
    assert response_info.data_id == response_post.data_id


@pytest.mark.asyncio
async def test_info_async(input_bytes):
    response_post = (await data_api.post_data_async(SERVER_URL, input_bytes)).unwrap()
    response_info = (
        await data_api.info_async(SERVER_URL, response_post.data_id)
    ).unwrap()

    assert response_info.code == 0
    assert response_info.data_id != "0"
    assert response_info.data_id != ""
    assert response_info.data_id == response_post.data_id
