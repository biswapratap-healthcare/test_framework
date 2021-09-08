import os
import shutil
import tempfile
import argparse
from threading import Thread

from combinatorics import get_all_combinations
from endpoints import endpoints


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
    parser.add_argument('-a',
                        '--agents',
                        help='The agents to be considered for this run - '
                             'ultimateALPR,openALPR,plateRecognizer',
                        required=True)
    args = parser.parse_args()
    raw_dir = args.raw_dir
    ground_truth_csv = args.ground_truth
    agents = args.agents.split(',')

    payload_dir = tempfile.mkdtemp()
    raw_images_zip_file_path = os.path.join(payload_dir, 'raw_images')
    ground_truth_csv_file_path = os.path.join(payload_dir, 'gt.csv')
    shutil.make_archive(raw_images_zip_file_path, 'zip', raw_dir)
    shutil.copy(ground_truth_csv, ground_truth_csv_file_path)
    work_dir = tempfile.mkdtemp()
    payload_zip_file_path = os.path.join(work_dir, 'payload')
    shutil.make_archive(payload_zip_file_path, 'zip', payload_dir)

    for k, v in endpoints.items():
        if k in agents:
            destination_dir = k
            thread = Thread(target=v, args=(destination_dir, payload_zip_file_path + '.zip'))
            thread.start()
            thread.join()
    shutil.rmtree(payload_dir)
    shutil.rmtree(work_dir)

    combinations = get_all_combinations()

    for combination in combinations:
        print("OCR : " + combination[0][0] + ", ROI : " + combination[1][0])
        ocr_csv = combination[0][1]
        roi_dir = combination[1][1]
        # TODO --> Call Vinuta's Script
