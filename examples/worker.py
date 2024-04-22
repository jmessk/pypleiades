from pymec_client.mec_worker import MECWorker
import logging


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s]:[%(funcName)s()]: %(message)s",
    )

    try:
        server_url = "https://mecrm.dolylab.cc/api/v0.5"

        # Create a worker
        worker = MECWorker(server_url)
        # Register the worker
        worker.register(
            [
                "pymec+echo",
            ]
        )
        # Wait for a job
        while (job := worker.contract()) is None:
            pass

        # Get the lambda and input data
        _, input_data = job.get_lambda_and_input_data()

        # Process the data
        output_data = f"{input_data}, World!"

        # Finish the job
        job.finish(output_data)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
