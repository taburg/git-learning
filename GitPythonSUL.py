import os
from typing import Union

from aalpy.base import SUL
from git import Repo

from utils import clean_up, create_file, change_file, delete_file


class GitWrapper:
    def __init__(self, repo_path, bare_repo_path):
        self.repo_path = repo_path
        self.bare_repo_path = bare_repo_path

        self.bare_repo: Repo = Repo.init(self.bare_repo_path, bare=True)
        assert self.bare_repo.bare
        # self.repo = Repo.init(self.repo_path)
        self.repo: Repo = self.bare_repo.clone(self.repo_path)
        assert os.path.exists(self.repo_path)
        assert not self.repo.bare
        # self.repo.create_remote('origin', self.bare_repo_path)

        self.commit_number = 0
        self.tag_number = 0
        self.branches = {'master': self.repo.active_branch}

    def current_branch(self):
        return 'BRANCH ' + str(self.repo.active_branch)

    def untracked(self):
        return 'UNTRACKED ' + str(len(self.repo.untracked_files))

    def is_dirty(self):
        return 'DIRTY' if self.repo.is_dirty() else 'NOT_DIRTY'

    def modified(self):
        return str(len(self.repo.index.diff(None)))

    def add(self, file: str):
        return self.add_all([file])

    def add_all(self, files: list[str]):
        try:
            self.repo.index.add(files)
            return True
        except Exception:
            return False

    def commit(self, allow_empty_commit):
        if not allow_empty_commit and not self.repo.is_dirty():
            return False
        try:
            self.repo.index.commit(f'Commit Number: {self.commit_number}')
            self.commit_number += 1
            return True
        except Exception:
            return False

    def tag(self):
        try:
            self.repo.create_tag(f'v.{self.tag_number}')
            self.tag_number += 1
            return True
        except Exception:
            return False

    def fetch(self):
        try:
            origin = self.repo.remotes.origin
            origin.fetch()
            return True
        except Exception:
            return False

    def pull(self):
        try:
            origin = self.repo.remotes.origin
            origin.pull()
            return True
        except Exception:
            return False

    def push(self):
        try:
            origin = self.repo.remotes.origin
            origin.push().raise_if_error()
            return True
        except Exception:
            return False

    def create_branch(self, branch_name):
        if branch_name in self.branches:
            return False
        try:
            new_branch = self.repo.create_head(branch_name, 'HEAD')
            self.repo.head.reference = new_branch
            self.repo.head.reset(index=True, working_tree=True)
            self.branches[branch_name] = new_branch
            return True
        except Exception:
            return False

    def checkout(self, branch_name):
        try:
            self.repo.head.reference = self.branches[branch_name]
            self.repo.head.reset(index=True, working_tree=True)
            return True
        except Exception:
            return False


class GitPythonSUL(SUL):
    def __init__(self, repo_path, bare_repo_path, change_uses_random_test=True, allow_empty_commit=False, verbose=True):
        super().__init__()
        self.repo_path = os.path.abspath(repo_path)
        self.bare_repo_path = os.path.abspath(bare_repo_path)
        assert not os.path.exists(self.repo_path)
        assert not os.path.exists(self.bare_repo_path)

        self.change_uses_random_test = change_uses_random_test
        self.allow_empty_commit = allow_empty_commit

        self.filenames: list[str] = ['file0.txt', 'file1.txt']

        self.branches = ['master', 'other_branch']

        self.git: Union[GitWrapper, None] = None

        self.verbose = verbose

    def pre(self):
        self.git = GitWrapper(self.repo_path, self.bare_repo_path)

    def post(self):
        clean_up(self.git, self.repo_path, self.bare_repo_path)

    def query(self, word: tuple) -> list:
        outputs = super(GitPythonSUL, self).query(word)
        if self.verbose:
            print(f'Current query and outputs: {list(zip(word, outputs))}')
        return outputs

    def step(self, letter):
        command_status = None
        # File operations
        if letter == 'create_f0':
            command_status = create_file(self.repo_path + '/' + self.filenames[0])
        elif letter == 'create_f1':
            command_status = create_file(self.repo_path + '/' + self.filenames[1])
        elif letter == 'change_f0':
            command_status = change_file(self.repo_path + '/' + self.filenames[0],
                                         use_random_text=self.change_uses_random_test)
        elif letter == 'change_f1':
            command_status = change_file(self.repo_path + '/' + self.filenames[1],
                                         use_random_text=self.change_uses_random_test)
        elif letter == 'delete_f0':
            command_status = delete_file(self.repo_path + '/' + self.filenames[0])
        elif letter == 'delete_f1':
            command_status = delete_file(self.repo_path + '/' + self.filenames[1])

        # # Git status checks
        # elif letter == 'branch':
        #     return self.git.current_branch()
        # elif letter == 'untracked':
        #     return self.git.untracked()
        # elif letter == 'dirty':
        #     return self.git.is_dirty()
        # elif letter == 'modified':
        #     return self.git.modified()

        # Git commands
        elif letter == 'add_all':
            command_status = self.git.add('.')
        elif letter == 'add_f0':
            command_status = self.git.add(self.filenames[0])
        elif letter == 'add_f1':
            command_status = self.git.add(self.filenames[1])
        elif letter == 'commit':
            command_status = self.git.commit(self.allow_empty_commit)
        elif letter == 'tag':
            command_status = self.git.tag()
        elif letter == 'fetch':
            command_status = self.git.fetch()
        elif letter == 'pull':
            command_status = self.git.pull()
        elif letter == 'push':
            command_status = self.git.push()
        elif letter == 'create_branch':
            command_status = self.git.create_branch(self.branches[1])
        elif letter == 'checkout_branch':
            command_status = self.git.checkout(self.branches[1])
        elif letter == 'checkout_master':
            command_status = self.git.checkout(self.branches[0])
        else:
            raise ValueError(f'This letter is not part of the alphabet! Letter: {letter}')

        return 'PASS' if command_status else 'FAIL'
