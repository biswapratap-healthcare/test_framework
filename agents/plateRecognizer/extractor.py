import os
import shutil
import tempfile
import zipfile
import pandas as pd
import requests
from PIL import Image


def run_platerecognizer_alpr(destination_dir, payload):
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
        with open(img_path, 'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                files=dict(upload=fp),
                headers={'Authorization': 'Token 6696c357b001ffead6348603430c55eee804fc4c'})
        resp = response.json()
        roi = resp['results'][0]['box']
        ocr = resp['results'][0]['plate']
        confidence = resp['results'][0]['score']
        df.at[idx, "ID"] = ''.join(image.split('.')[:-1])
        df.at[idx, "OCR"] = ocr
        df.at[idx, "Confidence"] = str(confidence)
        im = Image.open(img_path)
        im = im.crop((roi['xmin'], roi['ymin'], roi['xmax'], roi['ymax']))
        cropped_image_path = os.path.join(cropped_image_dir, image)
        im.save(cropped_image_path)
    shutil.make_archive(os.path.join(destination_dir, 'roi'), 'zip', cropped_image_dir)
    df.to_csv(os.path.join(destination_dir, 'gt_ocr.csv'))
    shutil.make_archive(destination_dir, 'zip', destination_dir)
    shutil.move(destination_dir + '.zip', os.path.join('output', destination_dir + '.zip'))
    shutil.rmtree(destination_dir)
    shutil.rmtree(cropped_image_dir)
    shutil.rmtree(raw_images_dir)
    shutil.rmtree(payload_root_dir)
