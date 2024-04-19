
from mec_client import MECClient
from swagger_client import ApiClient


def main():
    client = ApiClient()
    worker = MECClient(client=client)
    worker.register()

if __name__ == '__main__':
    main()
