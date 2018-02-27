import os

def fix_path(path, is_dir=True):
    base_path = os.getcwd()
    path = os.path.join(base_path, path)
    path = os.path.abspath(os.path.realpath(path))
    if is_dir:
        path = path + "/"
    return path