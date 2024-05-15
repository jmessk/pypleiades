import pytest

from pymec.api.data_api import DataAPI


SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


@pytest.fixture(scope="module")
def data_api() -> DataAPI:
    return DataAPI(SERVER_URL)


@pytest.fixture(scope="module")
def input_bytes():
    return b"Hello, World!"


def test_post_data(data_api, input_bytes):
    response_post = data_api.post_data(input_bytes).unwrap()

    assert response_post.code == 0
    assert response_post.data_id != "0"
    assert response_post.data_id != ""


@pytest.mark.asyncio
async def test_post_data_async(data_api, input_bytes):
    response_post = (await data_api.post_data_async(input_bytes)).unwrap()

    assert response_post.code == 0
    assert response_post.data_id != "0"
    assert response_post.data_id != ""


def test_get_data(data_api, input_bytes):
    response_post = data_api.post_data(input_bytes).unwrap()
    response_get = data_api.get_data(response_post.data_id).unwrap()

    assert response_get == input_bytes


@pytest.mark.asyncio
async def test_get_data_async(data_api, input_bytes):
    response_post = (await data_api.post_data_async(input_bytes)).unwrap()
    response_get = (
        await data_api.get_data_async(response_post.data_id)
    ).unwrap()

    assert response_get == input_bytes


def test_info(data_api, input_bytes):
    response_post = data_api.post_data(input_bytes).unwrap()
    response_info = data_api.info(response_post.data_id).unwrap()

    assert response_info.code == 0
    assert response_info.data_id != "0"
    assert response_info.data_id != ""
    assert response_info.data_id == response_post.data_id


@pytest.mark.asyncio
async def test_info_async(data_api, input_bytes):
    response_post = (await data_api.post_data_async(input_bytes)).unwrap()
    response_info = (
        await data_api.info_async(response_post.data_id)
    ).unwrap()

    assert response_info.code == 0
    assert response_info.data_id != "0"
    assert response_info.data_id != ""
    assert response_info.data_id == response_post.data_id
