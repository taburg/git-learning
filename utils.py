import os
import shutil


def create_file(path: str) -> bool:
    try:
        with open(path, 'x'):
            pass
        return True
    except Exception:
        return False


def change_file(path: str) -> bool:
    try:
        if not os.path.isfile(path):
            raise FileNotFoundError
        with open(path, 'a') as f:
            f.write("Some text" + '\n')
        return True
    except Exception:
        return False


def delete_file(path: str) -> bool:
    try:
        os.remove(path)
        return True
    except Exception:
        return False


def clean_up(git_instance, repo_path, bare_repo_path):
    if git_instance:
        git_instance.repo.close()

    for git_folder in [repo_path, bare_repo_path]:
        if os.path.exists(git_folder):
            os.chmod(git_folder, 0o777)
            for root, dirs, files in os.walk(git_folder):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o777)
                for f in files:
                    os.chmod(os.path.join(root, f), 0o777)

            shutil.rmtree(git_folder)
