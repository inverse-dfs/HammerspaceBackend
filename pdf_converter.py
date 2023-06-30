import subprocess
from os.path import exists

def convert_to_jpg(filename):
    jpg_name = filename.rsplit('.', 1)[0]
    print("")
    print("")
    print("")
    print("")
    print(jpg_name, filename)
    print("")
    print("")
    print("")
    print("")
    subprocess.run(["pdftoppm", "-jpeg", "-r", "300", filename, jpg_name])
    if not exists(jpg_name):
        jpg_name = filename.rsplit('.', 1)[0] + '-1.jpg'
    subprocess.run(["chmod 077 ", jpg_name])
    return jpg_name