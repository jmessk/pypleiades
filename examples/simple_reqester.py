from pymec_client.mec_requester import MECRequester
from pymec_client.mec_developer import MECDeveloper
import time
import logging


def get_lambda_id(server_url: str, runtime: str) -> str:
    # Create a developer
    developer = MECDeveloper(server_url)

    # Post lambda code and create a lambda
    lambda_data_id = developer.post_data(b"dummy lambda")
    lambda_id = developer.create_lambda(lambda_data_id, runtime)

    return lambda_id


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s]:[%(module)s::%(funcName)s()]: %(message)s",
    )

    try:
        server_url = "https://mecrm.dolylab.cc/api/v0.5"

        # Get the lambda id
        lambda_id = get_lambda_id(server_url, "pymec+echo")

        # Create a requester
        requester = MECRequester(server_url)

        # Post input data
        input_data_id = requester.post_data(b"Hello")

        # Create a job
        job = requester.create_job(lambda_id, input_data_id)
        # print(job.get_info())

        # Wait until the job is finished
        while not job.is_finished():
            time.sleep(0.1)

        # Get the output data
        output = job.get_output_data()
        print(output)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
