import logging
from pymec.mec_client import MECClient


SERVER_URL = "http://192.168.168.127:8332/api/v0.5"


def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a client
    client = MECClient(SERVER_URL, logger=logger)

    # Create a lambda
    lambda_ = (
        client.new_lambda()
        .set_code(client.new_blob().from_bytes(b"pymec+example"))
        .set_runtime("pymec+example")
    )

    # Create a input blob
    input_blob = client.new_blob().from_bytes(b"Hello")

    # Create a job by lambda id and input data bytes
    job = (
        client.new_job()
        .set_lambda(lambda_)
        .set_input(input_blob)
        .set_tags(["python3.10"])
        .run()
    )

    # Wait until the job is finished
    output_bytes = job.wait_for_finish(sleep_s=0.1).output_bytes()
    print(output_bytes)


if __name__ == "__main__":
    main()
