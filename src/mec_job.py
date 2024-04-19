import swagger_client
from mec_io import MECIO, MECResStatus


class MECJob(MECIO):
    def __init__(self, job_id):
        super().__init__(swagger_client.ApiClient())
        self._job_api = swagger_client.JobApi(self._client)
        self.job_id = job_id
    
    