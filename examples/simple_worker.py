import logging
from pymec.mec_client import MECClient


# SERVER_URL = "http://192.168.168.127:8332/api/v0.5"
SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a client
    client = MECClient(SERVER_URL, logger=logger)

    # Create a worker
    worker = (
        client.new_worker()
        .set_runtimes(
            [
                "pymec+echo",
                "pymec+echo+python3.10",
                "pymec+echo+example_worker",
            ]
        )
        .register()
        .set_tags(["python3.10"])
    )

    # Wait for a job
    job = worker.wait_contract()

    # Get the input data
    input_bytes = job.input_bytes()
    _ = job.lambda_bytes()

    # Process the data
    input_data = input_bytes.decode("utf-8")
    output_data = f"{input_data}, World!".encode("utf-8")

    # create output blob
    output_blob = client.new_blob().from_bytes(output_data)

    # Finish the job and send the output data to the requester
    job.finish(output_blob)


if __name__ == "__main__":
    main()
