from pymec_client.mec_worker import MECWorker
import logging


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s]:[%(module)s::%(funcName)s()]: %(message)s",
    )

    server_url = "https://mecrm.dolylab.cc/api/v0.5"

    # Create a worker
    worker = MECWorker(server_url)

    # Register the worker
    worker.register(
        [
            "pymec+echo",
        ]
    )
    # print(worker.get_info())

    # Wait for a job
    while (job := worker.contract()) is None:
        pass

    # print(job.get_info())

    # Get the lambda and input data
    input_data = job.get_input_data()
    # _ = job.get_lambda_data()
    # _, input_data = job.get_lambda_and_input_data()

    # Process the data
    input_data = input_data.decode("utf-8")
    output_data = f"{input_data}, World!".encode("utf-8")
    
    # Finish the job and send the output data to the requester
    job.finish(output_data)


if __name__ == "__main__":
    main()
