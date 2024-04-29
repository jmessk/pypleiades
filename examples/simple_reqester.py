from pymec_client.mec_requester import MECRequester
from pymec_client.mec_developer import MECDeveloper
import time
import logging


def get_lambda_id(server_url: str, runtime: str) -> str:
    # Create a developer
    developer = MECDeveloper(server_url)

    # Create a lambda
    lambda_id = developer.create_lambda_by_bytes(b"dummy lambda", runtime)

    return lambda_id


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s]:[%(module)s::%(funcName)s()]: %(message)s",
    )

    server_url = "https://mecrm.dolylab.cc/api/v0.5"

    # Get the lambda id
    lambda_id = get_lambda_id(server_url, "pymec+echo")

    # Create a requester
    requester = MECRequester(server_url)

    # Create a job by lambda id and input data bytes
    job = requester.create_job_by_bytes(lambda_id, b"Hello")
    # print(job.get_info())

    # Wait until the job is finished
    while not job.is_finished():
        time.sleep(0.1)

    # Get the output data
    output = job.get_output_data()
    print(output)


if __name__ == "__main__":
    main()
