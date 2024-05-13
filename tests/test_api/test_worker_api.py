import pytest

from pymec.api import (
    data_api,
    lambda_api,
    job_api,
    worker_api,
)


SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


# 毎回実行する
@pytest.fixture(autouse=True)
def job_id_1():
    data_id = data_api.post_data(SERVER_URL, b"pymec test lambda").unwrap().data_id
    lambda_id = (
        lambda_api.create(SERVER_URL, data_id, "pymec+pytest").unwrap().lambda_id
    )
    input_data_id = data_api.post_data(SERVER_URL, b"pymec test input").unwrap().data_id

    return job_api.create(SERVER_URL, lambda_id, input_data_id, []).unwrap().job_id


@pytest.fixture
def job_id_2():
    data_id = data_api.post_data(SERVER_URL, b"pymec test lambda").unwrap().data_id
    lambda_id = (
        lambda_api.create(SERVER_URL, data_id, "pymec+pytest+python3.10")
        .unwrap()
        .lambda_id
    )
    input_data_id = data_api.post_data(SERVER_URL, b"pymec test input").unwrap().data_id

    return job_api.create(SERVER_URL, lambda_id, input_data_id, []).unwrap().job_id


@pytest.fixture
def runtimes():
    return ["pymec+pytest", "pymec+pytest+python3.10"]


@pytest.fixture
def output_data_id():
    return data_api.post_data(SERVER_URL, b"pymec test output").unwrap().data_id


def test_register(runtimes):
    response = worker_api.register(SERVER_URL, runtimes).unwrap()

    assert response.code == 0


@pytest.mark.asyncio
async def test_register_async(runtimes):
    response = (await worker_api.register_async(SERVER_URL, runtimes)).unwrap()

    assert response.code == 0


def test_contract(job_id_1, runtimes):
    worker_id = worker_api.register(SERVER_URL, runtimes).unwrap().worker_id
    response_contract = worker_api.contract(SERVER_URL, worker_id, [], 10).unwrap()

    assert response_contract.code == 0
    assert response_contract.job_id == job_id_1


@pytest.mark.asyncio
async def test_contract_async(job_id_1, runtimes):
    worker_id = (
        (await worker_api.register_async(SERVER_URL, runtimes)).unwrap().worker_id
    )
    response_contract = (
        await worker_api.contract_async(SERVER_URL, worker_id, [], 10)
    ).unwrap()

    assert response_contract.code == 0
    assert response_contract.job_id == job_id_1


def test_info(runtimes):
    worker_id = worker_api.register(SERVER_URL, runtimes).unwrap().worker_id
    response_info = worker_api.info(SERVER_URL, worker_id).unwrap()

    assert response_info.code == 0
    assert response_info.worker_id == worker_id
    assert response_info.runtimes == runtimes


@pytest.mark.asyncio
async def test_info_async(runtimes):
    worker_id = (
        (await worker_api.register_async(SERVER_URL, runtimes)).unwrap().worker_id
    )
    response_info = (await worker_api.info_async(SERVER_URL, worker_id)).unwrap()

    assert response_info.code == 0
    assert response_info.worker_id == worker_id
    assert response_info.runtimes == runtimes
