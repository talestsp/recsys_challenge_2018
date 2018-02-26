import os

def fix_path(path):
    base_path = os.getcwd()
    path = os.path.join(base_path, path)
    path = os.path.abspath(os.path.realpath(path)) + "/"
    return path