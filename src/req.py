from mec_requester import MECRequester
from mec_job import MECJobStatus
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
        status, message = job.get_status()
        print(message)

        if status == MECJobStatus.FINISHED:
            break
            
        time.sleep(1)



if __name__ == '__main__':
    main()
