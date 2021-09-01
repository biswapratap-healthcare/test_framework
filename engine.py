import requests
from time import sleep


def run_engine(job_id, endpoint):
    endpoint_splits = endpoint.split('/')
    get_percent_endpoint = '/'.join(endpoint_splits[:-1]) + '/get_progress'
    values = {'job_id': job_id}
    r = requests.post(get_percent_endpoint, data=values)
    while r.text == '100':
        sleep(1)
        r = requests.post(get_percent_endpoint, data=values)
    download_result_endpoint = '/'.join(endpoint_splits[:-1]) + '/get_extracted_data'
    values = {'job_id': job_id}
    r = requests.post(download_result_endpoint, data=values)
