import httpx


SERVER_URL = "https://mecrm.dolylab.cc/api/v0.5"


def create_namespace():
    endpoint = f"{SERVER_URL}/kv"

    with httpx.Client() as client:
        response = client.post(endpoint)

    response_json = response.json()
    print(response_json)

    # {'code': 0, 'status': 'ok', 'id': '57518271858999296'}
    return response_json


if __name__ == "__main__":
    create_namespace()
