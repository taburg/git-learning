import os
import shutil
import string
import time
from random import random


def create_file(path: str) -> bool:
    try:
        with open(path, 'x'):
            pass
        return True
    except Exception:
        return False


def change_file(path: str, use_random_text=True) -> bool:
    try:
        if not os.path.isfile(path):
            raise FileNotFoundError
        with open(path, 'a') as f:
            if use_random_text:
                text = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
            else:
                text = 'Lorem ipsum'
            f.write(text + '\n')
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

    num_deletion_tries = 0

    while num_deletion_tries < 5:
        try:
            for git_folder in [repo_path, bare_repo_path]:
                if os.path.exists(git_folder):
                    os.chmod(git_folder, 0o777)
                    for root, dirs, files in os.walk(git_folder):
                        for d in dirs:
                            os.chmod(os.path.join(root, d), 0o777)
                        for f in files:
                            os.chmod(os.path.join(root, f), 0o777)

                    shutil.rmtree(git_folder)

            return

        except Exception:
            print(f'Deletion error (most likely to dangling processes holding git files). {num_deletion_tries + 1}/5.')
            num_deletion_tries += 1
            time.sleep(1)