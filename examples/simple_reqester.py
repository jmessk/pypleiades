import logging
from pymec.pleiades_client import PleiadesClient


# SERVER_URL = "http://192.168.168.127:8332/api/v0.5"
SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


def main():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a client
    client = PleiadesClient(SERVER_URL, logger=logger)

    # Create a lambda
    lambda_ = (
        client.new_lambda()
        .set_code(client.new_blob().from_bytes(b"pymec echo"))
        .set_runtime("pymec+echo")
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
        .wait_for_finish(sleep_s=0.1)
    )

    # Get the output data
    print(job.output.data)


if __name__ == "__main__":
    main()
