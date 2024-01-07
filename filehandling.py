import os


def create_file(path: str) -> str:
    try:
        with open(path, 'x') as f:
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
