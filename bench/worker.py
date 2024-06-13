from pymec import PleiadesClient
import logging
import threading

from test_timer import Timer


SERVER_URL = "http://192.168.168.127:8332/api/v0.5"
# SERVER_URL = "http://172.21.39.32:8332/api/v0.5"
# SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


logger = logging.getLogger("pymec")
logger.setLevel(logging.ERROR)


q_flag = False


def q_thread():
    global q_flag
    while True:
        q = input()
        if q == "q":
            q_flag = True
            break


t = threading.Thread(target=q_thread)
t.start()


def main():
    # Create a client
    client = PleiadesClient(SERVER_URL, logger=logger)

    # Create a worker
    worker = (
        client.new_worker()
        .set_runtimes(
            [
                "pymec+hello",
            ]
        )
        .register()
        .set_tags(["python3.10"])
    )

    while not q_flag:
        # Wait for a job
        t = Timer("wait_contract")
        job = worker.contract(timeout_s=5)
        if job is None:
            t.finish()
            continue

        # _ = job.lambda_.blob.data

        # Process the data
        # t = Timer("process")
        input_data = job.get_input().get_data().decode("utf-8")
        output_data = f"{input_data}, MEC-RM!".encode("utf-8")
        # t.finish()

        # create output blob
        # t = Timer("output_blob")
        output_blob = client.new_blob().from_bytes(output_data).upload()
        # t.finish()

        # Finish the job and send the output data to the requester
        # t = Timer("finish")
        job.finish(output_blob)
        t.finish()


if __name__ == "__main__":
    main()
