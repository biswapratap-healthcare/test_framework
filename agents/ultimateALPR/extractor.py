import json
import os
import shutil
import tempfile
import zipfile
import pandas as pd
from PIL import Image


def run_ultimate_alpr(destination_dir, payload):
    payload_root_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(payload, 'r') as zip_ref:
        zip_ref.extractall(payload_root_dir)
    raw_images_zip_path = os.path.join(payload_root_dir, 'raw_images.zip')
    gt_csv_file_path = os.path.join(payload_root_dir, 'gt.csv')
    df = pd.read_csv(gt_csv_file_path)
    df["ID"] = ""
    df["OCR"] = ""
    df["Confidence"] = ""
    raw_images_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(raw_images_zip_path, 'r') as zip_ref:
        zip_ref.extractall(raw_images_dir)
    images = os.listdir(raw_images_dir)
    cropped_image_dir = tempfile.mkdtemp()
    for idx, image in enumerate(images):
        img_path = os.path.join(raw_images_dir, image)
        os.environ["PYTHONPATH"] = "./agents/ultimateALPR/ultimateALPR/binaries/windows/x86_64;" \
                                   "./agents/ultimateALPR/ultimateALPR/python"
        cmd = 'python ./agents/ultimateALPR/ultimateALPR/samples/python/recognizer/recognizer.py --image "' \
              + img_path + '" --assets ./agents/ultimateALPR/ultimateALPR/assets > out.txt'
        os.system(cmd)
        with open('out.txt', 'r') as f:
            lines = f.readlines()
            json_string = lines[1][34:]
            json_obj = json.loads(json_string)
            ocr = json_obj['plates'][0]['text']
            confidence = max(json_obj['plates'][0]['confidences'])
            df.at[idx, "ID"] = ''.join(image.split('.')[:-1])
            df.at[idx, "OCR"] = ocr
            df.at[idx, "Confidence"] = str(confidence)
            roi = json_obj['plates'][0]['warpedBox']
            im = Image.open(img_path)
            im = im.crop((roi[0], roi[1], roi[4], roi[5]))
            cropped_image_path = os.path.join(cropped_image_dir, image)
            im.save(cropped_image_path)
        os.remove('out.txt')
    shutil.make_archive(os.path.join(destination_dir, 'roi'), 'zip', cropped_image_dir)
    df.to_csv(os.path.join(destination_dir, 'gt_ocr.csv'))
    shutil.make_archive(destination_dir, 'zip', destination_dir)
    shutil.move(destination_dir + '.zip', os.path.join('output', destination_dir + '.zip'))
    shutil.rmtree(destination_dir)
    shutil.rmtree(cropped_image_dir)
    shutil.rmtree(raw_images_dir)
    shutil.rmtree(payload_root_dir)
