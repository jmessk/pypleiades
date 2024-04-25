from pymec_client.mec_requester import MECRequester
import time
import logging


"""
# Info

この例では `requester.create_lambda()` で Requester が Lambda を作成していますが、
本来はサービスの開発者(Developer)が Lambda を作成し、
利用者はその Lambda を利用することが想定されています。
"""


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s]:[%(module)s::%(funcName)s()]: %(message)s",
    )

    try:
        server_url = "https://mecrm.dolylab.cc/api/v0.5"

        # Create a requester
        requester = MECRequester(server_url)

        # Post lambda code and create a lambda
        lambda_data_id = requester.post_data("dummy lambda")
        lambda_id = requester.create_lambda(lambda_data_id, "pymec+echo")

        # Post input data
        input_data_id = requester.post_data("Hello")

        # Create a job
        job = requester.create_job(lambda_id, input_data_id)
        print(job.get_info())

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
