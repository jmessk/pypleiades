from pymec import PleiadesClient
import logging


# SERVER_URL = "http://192.168.168.127:8332/api/v0.5"
SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5-snapshot"


def main():
    # Create a client
    client = PleiadesClient(SERVER_URL)

    # New namespace instance in local
    namespace = client.new_kv_namespace()

    # Create a namespace in remote
    namespace.create()

    # or you can select existing namespace
    # namespace.set_namespace_id("<namespace_id>")

    # New key handler
    key_1 = namespace.new_key("key-1")

    # Set value
    key_1.set("Hello, World!")

    # Get value
    for _ in range(3):
        print(key_1.get())

    # other key
    value = namespace.new_key("key-2").set("Other value").get()
    print(value)


if __name__ == "__main__":
    main()
