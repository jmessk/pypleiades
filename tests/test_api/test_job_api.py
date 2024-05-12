import pytest
import logging.config
import logging

from pymec.api import data_api
from pymec.api import lambda_api
from pymec.api import job_api


SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


@pytest.fixture
def lambda_id():
    data = data_api.post_data(SERVER_URL, b"pymec test lambda").unwrap()
    return lambda_api.create(SERVER_URL, data.data_id, "pymec+pytest").unwrap().lambda_id


@pytest.fixture
def input_data_id():
    return data_api.post_data(SERVER_URL, b"pymec test input").unwrap().data_id


@pytest.fixture
def output_data_id():
    return data_api.post_data(SERVER_URL, b"pymec test output").unwrap().data_id


@pytest.fixture
def tags():
    return ["python3.10"]


def test_create(lambda_id, input_data_id, tags):
    response_create = job_api.create(
        SERVER_URL, lambda_id, input_data_id, tags
    ).unwrap()

    assert response_create.code == 0
    assert response_create.job_id != "0"
    assert response_create.job_id != ""


@pytest.mark.asyncio
async def test_create_async(lambda_id, input_data_id, tags):
    response_create = (
        await job_api.create_async(SERVER_URL, lambda_id, input_data_id, tags)
    ).unwrap()

    assert response_create.code == 0
    assert response_create.job_id != "0"
    assert response_create.job_id != ""


def test_info(lambda_id, input_data_id, tags):
    response_create = job_api.create(
        SERVER_URL, lambda_id, input_data_id, tags
    ).unwrap()

    response_info = job_api.info(SERVER_URL, response_create.job_id).unwrap()

    assert response_info.code == 0
    assert response_info.job_id == response_create.job_id
    assert response_info.lambda_.lambda_id == lambda_id
    assert response_info.input.data_id == input_data_id
    # assert response_info.tags == tags


@pytest.mark.asyncio
async def test_info_async(lambda_id, input_data_id, tags):
    response_create = (
        await job_api.create_async(SERVER_URL, lambda_id, input_data_id, tags)
    ).unwrap()

    response_info = (
        await job_api.info_async(SERVER_URL, response_create.job_id)
    ).unwrap()

    assert response_info.code == 0
    assert response_info.job_id == response_create.job_id
    assert response_info.lambda_.lambda_id == lambda_id
    assert response_info.input.data_id == input_data_id
    # assert response_info.tags == tags


def test_update(lambda_id, input_data_id, tags, output_data_id):
    response_create = job_api.create(
        SERVER_URL, lambda_id, input_data_id, tags
    ).unwrap()

    response_update = job_api.update(
        SERVER_URL, response_create.job_id, output_data_id, "finished"
    ).unwrap()

    assert response_update.code == 0

    response_info = job_api.info(SERVER_URL, response_create.job_id).unwrap()

    assert response_info.job_status == "Finished"


@pytest.mark.asyncio
async def test_update_async(lambda_id, input_data_id, tags, output_data_id):
    response_create = (
        await job_api.create_async(SERVER_URL, lambda_id, input_data_id, tags)
    ).unwrap()

    response_update = (
        await job_api.update_async(
            SERVER_URL, response_create.job_id, output_data_id, "finished"
        )
    ).unwrap()

    assert response_update.code == 0

    response_info = (
        await job_api.info_async(SERVER_URL, response_create.job_id)
    ).unwrap()

    assert response_info.job_status == "Finished"
