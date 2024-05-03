from pymec_client.mec_developer import MECDeveloper
from pymec_client.mec_requester import MECRequester

from pymec_client.pleiades_api import MECAPI


SERVER_URL = "http://192.168.168.127:8332/api/v0.5"


developer = MECDeveloper(SERVER_URL)
api = MECAPI(SERVER_URL)
# lambda_id = developer.create_lambda_by_bytes(b"dummy lambda", "pymec+test")

lambda_data_id = developer.post_data(b"test lambda data")
print(lambda_data_id)

lambda_id = developer.create_lambda_by_id(lambda_data_id, "pymec+test")
print(lambda_id)
print(api.get_lambda_metadata(lambda_id))


requester = MECRequester(SERVER_URL)

job = requester.create_job_by_bytes(lambda_id, b"Hello")

print(job.get_info())
