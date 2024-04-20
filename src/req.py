from mec_requester import MECRequester
from swagger_client import ApiClient
import time


def main():
    client = ApiClient()
    requester = MECRequester(client)

    lambda_data_id = requester.post_data("./sample.txt")
    lambda_id = requester.create_lambda(lambda_data_id, "python+echo")

    input_data_id = requester.post_data("./sample.txt")

    job = requester.create_job(lambda_id, input_data_id)

    while True:
        if job.is_finished():
            break

        print(job.get_info())
        time.sleep(1)
    
    print(job.get_info())


if __name__ == "__main__":
    main()
