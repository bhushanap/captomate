import shutil
import os

def remove_folder(user):
    try:
        # Use shutil.rmtree to remove everything in /tmp
        shutil.rmtree(user, ignore_errors=True)
        print("Successfully removed everything from tmp")
    except PermissionError:
        print("Error: Permission denied to remove files in /tmp")

def make_folder(user):
    tmp_path = os.path.join(user,'tmp')
    cfg_path = os.path.join(user,'cfg')
    try:
        os.makedirs(tmp_path)
        os.makedirs(cfg_path)
        print("Successfully removed everything from output")
    except PermissionError:
        print("Error: Permission denied to remove files in /output")
