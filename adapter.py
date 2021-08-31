import os
import shutil
import tempfile
import argparse
import requests as requests
from threading import Thread

from engine import run_engine
from db_driver import get_endpoints


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r',
                        '--raw_dir',
                        help='The directory containing the raw images.',
                        required=True)
    parser.add_argument('-g',
                        '--ground_truth',
                        help='The CSV file containing the mapping of the '
                             'raw images to their associated ground truth labels.',
                        required=True)
    args = parser.parse_args()
    raw_dir = args.raw_dir
    ground_truth_csv = args.ground_truth

    payload_dir = tempfile.mkdtemp()
    raw_images_zip_file_path = os.path.join(payload_dir, 'raw_images')
    ground_truth_csv_file_path = os.path.join(payload_dir, os.path.basename(ground_truth_csv))
    shutil.make_archive(raw_images_zip_file_path, 'zip', raw_dir)
    shutil.copy(ground_truth_csv, ground_truth_csv_file_path)
    shutil.make_archive('payload', 'zip', payload_dir)

    shutil.rmtree(payload_dir)
    files = {'payload': open('payload.zip', 'rb')}
    endpoints = get_endpoints()
    for endpoint in endpoints:
        r = requests.post(endpoint, files=files)
        job_id = r.text
        thread = Thread(target=run_engine, args=(job_id,))
        thread.start()
        thread.join()
