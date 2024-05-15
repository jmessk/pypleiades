import pytest
import asyncio

from pymec.api.data_api import DataAPI
from pymec.api.lambda_api import LambdaAPI


SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


@pytest.fixture(scope="module")
def input_data_id():
    data_api = DataAPI(SERVER_URL)

    input_bytes = b"Hello, World!"
    response_post = data_api.post_data(input_bytes).unwrap()

    return response_post.data_id


@pytest.fixture(scope="module")
def runtime():
    return str("pymec+pytest")


@pytest.fixture(scope="module")
def lambda_api() -> LambdaAPI:
    return LambdaAPI(SERVER_URL)


def test_create(input_data_id, lambda_api, runtime):
    response_create = lambda_api.create(input_data_id, runtime).unwrap()

    assert response_create.code == 0
    assert response_create.lambda_id != "0"
    assert response_create.lambda_id != ""


@pytest.mark.asyncio
async def test_create_async(input_data_id, lambda_api, runtime):
    response_create = (
        await lambda_api.create_async(input_data_id, runtime)
    ).unwrap()

    assert response_create.code == 0
    assert response_create.lambda_id != "0"
    assert response_create.lambda_id != ""


def test_info(input_data_id, lambda_api, runtime):
    response_create = lambda_api.create(input_data_id, runtime).unwrap()
    response_info = lambda_api.info(response_create.lambda_id).unwrap()

    assert response_info.code == 0
    assert response_info.lambda_id == response_create.lambda_id
    assert response_info.data_id == input_data_id
    assert response_info.runtime == runtime


@pytest.mark.asyncio
async def test_info_async(input_data_id, lambda_api, runtime):
    response_create = (
        await lambda_api.create_async(input_data_id, runtime)
    ).unwrap()
    response_info = (
        await lambda_api.info_async(response_create.lambda_id)
    ).unwrap()

    assert response_info.code == 0
    assert response_info.lambda_id == response_create.lambda_id
    assert response_info.data_id == input_data_id
    assert response_info.runtime == runtime
