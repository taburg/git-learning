import os
import shutil


def create_file(path: str) -> str:
    try:
        with open(path, 'w'):
            pass
        return "CREATE_SUCCESS"
    except Exception:
        return "CREATE_FAIL"


def change_file(path: str) -> str:
    try:
        if not os.path.isfile(path):
            raise FileNotFoundError
        with open(path, 'a') as f:
            f.write("Some text" + '\n')
        return "WRITE_SUCCESS"
    except Exception:
        return "WRITE_FAIL"


def delete_file(path: str) -> str:
    try:
        os.remove(path)
        return "DELETE_SUCCESS"
    except Exception:
        return "DELETE_FAIL"


def clean_up(repo_path, bare_repo_path):
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    if os.path.exists(bare_repo_path):
        shutil.rmtree(bare_repo_path)
