import io
import json
import os
import zipfile

import requests
from time import sleep


def run_engine(job_id, endpoint):
    endpoint_splits = endpoint.split('/')
    get_percent_endpoint = '/'.join(endpoint_splits[:-1]) + '/get_progress'
    values = {'job_id': job_id}
    r = requests.post(get_percent_endpoint, data=values)
    percent = json.loads(r.text)["percent"]
    while percent != '100':
        print(percent)
        sleep(1)
        r = requests.post(get_percent_endpoint, data=values)
        percent = json.loads(r.text)["percent"]
    download_result_endpoint = '/'.join(endpoint_splits[:-1]) + '/get_extracted_data'
    values = {'job_id': job_id}
    os.mkdir(job_id)
    r = requests.post(download_result_endpoint, data=values)
    zip_handle = zipfile.ZipFile(io.BytesIO(r.content), "r")
    zip_handle.extractall(path=job_id)
    zip_handle.close()
