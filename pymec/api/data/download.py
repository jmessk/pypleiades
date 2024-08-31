from .. import api
import httpx


class Response(api.Response):
    data: bytes

    def from_response(response: httpx.Response):
        return Response(data=response.content)


class Request(api.Request[Response]):
    data_id: str

    def endpoint(self):
        return f"/data/{self.data_id}/blob"

    async def send(self, client: httpx.AsyncClient) -> Response:
        response = await client.get(self.endpoint())

        return Response.from_response(response)
