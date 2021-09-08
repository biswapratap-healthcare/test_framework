import os
import zipfile
import tempfile


def get_all_combinations():
    ocr_csv_paths = list()
    roi_dir_paths = list()
    work_dir = tempfile.mkdtemp()
    zips = os.listdir('output')
    for z in zips:
        sw = z_dir = z[:-4]
        z = os.path.join('output', z)
        d = os.path.join(work_dir, z_dir)
        os.mkdir(d)
        with zipfile.ZipFile(z, 'r') as zip_ref:
            zip_ref.extractall(d)
        contents = os.listdir(d)
        for content in contents:
            if '.csv' in content:
                ocr_csv_paths.append((sw, os.path.join(d, content)))
            else:
                temp_dir = tempfile.mkdtemp()
                with zipfile.ZipFile(os.path.join(d, content), 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                roi_dir_paths.append((sw, temp_dir))
    all_combinations = list()
    for ocr_csv_path in ocr_csv_paths:
        for roi_dir_path in roi_dir_paths:
            combination = (ocr_csv_path, roi_dir_path)
            all_combinations.append(combination)
    return all_combinations
