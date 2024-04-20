from mec_job import MECJob
from mec_worker import MECWorker
from swagger_client import ApiClient


def main():
    client = ApiClient()
    worker = MECWorker(client, ["python+echo"])

        
    while True:
        job = worker.contract()
        if job is not None:
            break
        print("No job.")

    _, input_data = job.get_lambda_and_data()
    
    output_data = f"Hello, {input_data}!"
    job.finish(output_data)


if __name__ == '__main__':
    main()
