import os

from git import Repo


class GitWrapper:
    def __init__(self, repo_path, bare_repo_path, mimic_cli_git_commit=False):
        self.mimic_cli_git_commit = mimic_cli_git_commit
        self.repo_path = repo_path
        self.bare_repo_path = bare_repo_path

        self.bare_repo: Repo = Repo.init(self.bare_repo_path, bare=True)
        assert self.bare_repo.bare
        # self.repo = Repo.init(self.repo_path)
        self.repo: Repo = self.bare_repo.clone(self.repo_path)
        assert not self.repo.bare
        # self.repo.create_remote('origin', self.bare_repo_path)

        self.commit_number = 0
        self.tag_number = 0
        self.branches = {'master': self.repo.active_branch}

    def current_branch(self):
        return "BRANCH " + str(self.repo.active_branch)

    def untracked(self):
        return "UNTRACKED " + str(len(self.repo.untracked_files))

    def is_dirty(self):
        return "DIRTY" if self.repo.is_dirty() else "NOT_DIRTY"

    def modified(self):
        return str(len(self.repo.index.diff(None)))

    def add(self, file: str):
        return self.add_all([file])

    def add_all(self, files: list[str]):
        try:
            self.repo.index.add(files)
            return "ADD_SUCCESS"
        except Exception:
            return "ADD_FAIL"

    def commit(self):
        if self.mimic_cli_git_commit and not self.repo.is_dirty():
            return "COMMIT_FAIL"
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

    def fetch(self):
        try:
            origin = self.repo.remotes.origin
            origin.fetch()
            return "FETCH_SUCCESS"
        except Exception:
            return "FETCH_FAIL"

    def pull(self):
        try:
            origin = self.repo.remotes.origin
            origin.pull()
            return "PULL_SUCCESS"
        except Exception:
            return "PULL_FAIL"

    def push(self):
        try:
            origin = self.repo.remotes.origin
            origin.push().raise_if_error()
            return "PUSH_SUCCESS"
        except Exception:
            return "PUSH_FAIL"

    def create_branch(self, branch_name):
        try:
            new_branch = self.repo.create_head(branch_name, "HEAD")
            self.repo.head.reference = new_branch
            self.repo.head.reset(index=True, working_tree=True)
            self.branches[branch_name] = new_branch
            return "BRANCH_SUCCESS"
        except Exception:
            return "BRANCH_FAIL"

    def checkout(self, branch_name):
        try:
            self.repo.head.reference = self.branches[branch_name]
            self.repo.head.reset(index=True, working_tree=True)
            return "CHECKOUT_SUCCESS"
        except Exception:
            return "CHECKOUT_FAIL"

    def destroy(self):
        os.system('rm -rf ' + self.repo_path)
        os.system('rm -rf ' + self.bare_repo_path)
