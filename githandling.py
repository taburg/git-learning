import os

from git import Repo


class GitWrapper:
    def __init__(self, repo_path, bare_repo_path):
        self.repo_path = repo_path
        self.bare_repo_path = bare_repo_path

        self.repo = Repo.init(self.repo_path)
        self.bare_repo = Repo.init(self.bare_repo_path, bare=True)
        assert not self.repo.bare
        assert self.bare_repo.bare
        # self.repo.create_remote('origin', self.bare_repo_path)

        self.commit_number = 0
        self.tag_number = 0

    def untracked(self):
        return "UNTRACKED " + str(len(self.repo.untracked_files))

    def is_dirty(self):
        return "DIRTY" if self.repo.is_dirty() else "NOT_DIRTY"

    def add(self, file: str):
        return self.add_all([file])

    def add_all(self, files: list[str]):
        try:
            self.repo.index.add(files)
            return "ADD_SUCCESS"
        except Exception:
            return "ADD_FAIL"

    def commit(self):
        try:
            self.repo.index.commit("Commit number " + str(self.commit_number))
            self.commit_number += 1
            return "COMMIT_SUCCESS"
        except Exception:
            return "COMMIT_FAIL"

    def tag(self):
        try:
            self.repo.create_tag('tag-' + str(self.tag_number))
            self.tag_number += 1
            return "TAG_SUCCESS"
        except Exception:
            return "TAG_FAIL"

    def destroy(self):
        os.system('rm -rf ' + self.repo_path)
        os.system('rm -rf ' + self.bare_repo_path)
