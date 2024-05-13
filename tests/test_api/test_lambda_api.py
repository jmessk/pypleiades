import pytest

from pymec.api import data_api, lambda_api


SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


@pytest.fixture
def input_data_id():
    input_bytes = b"Hello, World!"
    response_post = data_api.post_data(SERVER_URL, input_bytes).unwrap()

    return response_post.data_id


@pytest.fixture
def runtime():
    return str("pymec+pytest")


def test_create(input_data_id, runtime):
    response_create = lambda_api.create(SERVER_URL, input_data_id, runtime).unwrap()

    assert response_create.code == 0
    assert response_create.lambda_id != "0"
    assert response_create.lambda_id != ""


@pytest.mark.asyncio
async def test_create_async(input_data_id, runtime):
    response_create = (
        await lambda_api.create_async(SERVER_URL, input_data_id, runtime)
    ).unwrap()

    assert response_create.code == 0
    assert response_create.lambda_id != "0"
    assert response_create.lambda_id != ""


def test_info(input_data_id, runtime):
    response_create = lambda_api.create(SERVER_URL, input_data_id, runtime).unwrap()
    response_info = lambda_api.info(SERVER_URL, response_create.lambda_id).unwrap()

    assert response_info.code == 0
    assert response_info.lambda_id == response_create.lambda_id
    assert response_info.data_id == input_data_id
    assert response_info.runtime == runtime


@pytest.mark.asyncio
async def test_info_async(input_data_id, runtime):
    response_create = (
        await lambda_api.create_async(SERVER_URL, input_data_id, runtime)
    ).unwrap()
    response_info = (
        await lambda_api.info_async(SERVER_URL, response_create.lambda_id)
    ).unwrap()

    assert response_info.code == 0
    assert response_info.lambda_id == response_create.lambda_id
    assert response_info.data_id == input_data_id
    assert response_info.runtime == runtime
