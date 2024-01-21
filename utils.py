import os
import shutil


def create_file(path: str) -> str:
    try:
        with open(path, 'x'):
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


def clean_up(git_instance, repo_path, bare_repo_path):
    if git_instance:
        git_instance.repo.close()
        git_instance = None

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    if os.path.exists(bare_repo_path):
        os.chmod(bare_repo_path, 0o777)
        for root, dirs, files in os.walk(bare_repo_path):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o777)
            for f in files:
                os.chmod(os.path.join(root, f), 0o777)

        shutil.rmtree(bare_repo_path)

