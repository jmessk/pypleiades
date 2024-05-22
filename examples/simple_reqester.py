from pymec import PleiadesClient


# SERVER_URL = "http://192.168.168.127:8332/api/v0.5"
SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


def main():
    # Create a client
    client = PleiadesClient(SERVER_URL)

    # Create a lambda
    lambda_ = (
        client.new_lambda()
        .set_blob(client.new_blob().from_bytes(b"pymec echo"))
        .set_runtime("pymec+echo")
    )

    # Create a input blob
    input_blob = client.new_blob().from_bytes(b"Hello")

    # Create a job by lambda and input
    job = (
        client.new_job()
        .set_lambda(lambda_)
        .set_input(input_blob)
        .set_tags(["python3.10"])
        .run()
        .wait("Finished", 5)
    )

    # Get the output data
    print(job.get_output().get_data())


if __name__ == "__main__":
    main()
