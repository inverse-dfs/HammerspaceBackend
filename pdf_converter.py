import subprocess
from os.path import exists

def convert_to_jpg(filename):
    jpg_name = filename.rsplit('.', 1)[0] + '.jpeg'
    subprocess.run(["convert", filename, jpg_name])
    if not exists(jpg_name):
        jpg_name = filename.rsplit('.', 1)[0] + '-0.jpeg'
    return jpg_name