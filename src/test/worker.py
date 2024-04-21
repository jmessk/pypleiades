import sys

sys.path.append("../")

from mec_worker import MECWorker


def main():
    server_url = "https://mecrm.dolylab.cc/api/v0.5"
    worker = MECWorker(server_url, ["python+echo"])

    print(worker.get_info())

    # while True:
    #     job = worker.contract()

    #     if job is not None:
    #         break

    #     print("No job.")

    while (job := worker.contract()) is None:
        print("No job.")

    input_lambda, input_data = job.get_lambda_and_input_data()
    
    print(input_lambda, input_data)

    output_data = f"{input_data}, World!"

    job.finish(output_data)


if __name__ == "__main__":
    main()
