import sys

sys.path.append("../")

from mec_requester import MECRequester
import time


def main():
    server_url = "https://mecrm.dolylab.cc/api/v0.5"
    requester = MECRequester(server_url)

    lambda_data_id = requester.post_data("dummy lambda")
    lambda_id = requester.create_lambda(lambda_data_id, "python+echo")

    input_data_id = requester.post_data("Hello")

    job = requester.create_job(lambda_id, input_data_id)

    while True:
        if job.is_finished():
            break

        print(job.get_info())
        time.sleep(1)

    output = job.get_output_data()

    print(job.get_info())
    print(output)


if __name__ == "__main__":
    main()
