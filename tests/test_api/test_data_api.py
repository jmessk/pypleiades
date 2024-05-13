import pytest

from pymec.api.data_api import DataAPI


SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


@pytest.fixture
def api():
    return DataAPI(SERVER_URL)


@pytest.fixture
def input_bytes():
    return b"Hello, World!"


def test_post_data(api, input_bytes):
    response_post = api.post_data(input_bytes).unwrap()

    assert response_post.code == 0
    assert response_post.data_id != "0"
    assert response_post.data_id != ""


@pytest.mark.asyncio
async def test_post_data_async(api, input_bytes):
    response_post = (await api.post_data_async(SERVER_URL, input_bytes)).unwrap()

    assert response_post.code == 0
    assert response_post.data_id != "0"
    assert response_post.data_id != ""


def test_get_data(input_bytes):
    response_post = api.post_data(SERVER_URL, input_bytes).unwrap()
    response_get = api.get_data(SERVER_URL, response_post.data_id).unwrap()

    assert response_get == input_bytes


@pytest.mark.asyncio
async def test_get_data_async(input_bytes):
    response_post = (await api.post_data_async(SERVER_URL, input_bytes)).unwrap()
    response_get = (
        await api.get_data_async(SERVER_URL, response_post.data_id)
    ).unwrap()

    assert response_get == input_bytes


def test_info(input_bytes):
    response_post = api.post_data(SERVER_URL, input_bytes).unwrap()
    response_info = api.info(SERVER_URL, response_post.data_id).unwrap()

    assert response_info.code == 0
    assert response_info.data_id != "0"
    assert response_info.data_id != ""
    assert response_info.data_id == response_post.data_id


@pytest.mark.asyncio
async def test_info_async(input_bytes):
    response_post = (await api.post_data_async(SERVER_URL, input_bytes)).unwrap()
    response_info = (
        await api.info_async(SERVER_URL, response_post.data_id)
    ).unwrap()

    assert response_info.code == 0
    assert response_info.data_id != "0"
    assert response_info.data_id != ""
    assert response_info.data_id == response_post.data_id
