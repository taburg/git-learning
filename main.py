import os
import random

import aalpy
import git
from aalpy.base import SUL
from git import Repo


input_alphabet: list = [
    # File operations
    'create_file1',
    'create_file2',
    'change_file1',
    'change_file2',
    'delete_file1',
    'delete_file2',

    # Git commands
    'add_all',
    'add_file1',
    'add_file2',
    'commit',
    'fetch',
    'pull',
    'push',
    'tag'
]


def get_random_garbage() -> str:
    return str(random.choices(range(ord('A'), ord('Z')), k=random.randint(5, 25)))


class GitSUL(SUL):
    def __init__(self):
        super().__init__()
        self.repo_path: str = '/tmp/repo'
        self.bare_repo_path: str = '/tmp/barerepo.git'
        assert not os.path.exists(self.repo_path)
        assert not os.path.exists(self.bare_repo_path)
        self.repo: Repo | None = None
        self.bare_repo: Repo | None = None
        self.filenames: list = ['file0.txt', 'file1.txt']
        self.commit_number: int = -1
        self.tag_number: int = -1

    def pre(self):
        self.repo = Repo.init(self.repo_path)
        self.bare_repo = Repo.init(self.bare_repo_path, bare=True)
        assert not self.repo.bare
        assert self.bare_repo.bare
        self.repo.create_remote('origin', self.bare_repo_path)
        self.commit_number = -1
        self.tag_number = -1

    def post(self):
        os.rmdir(self.repo_path)
        os.rmdir(self.bare_repo_path)
        self.repo = None
        self.bare_repo = None

    def step(self, letter):
        match letter:
            # File operations
            case 'create_file0':  # TODO catch errors and return -1?
                with open(self.repo_path + '/' + self.filenames[0], 'x') as f:
                    pass
            case 'create_file1':
                with open(self.repo_path + '/' + self.filenames[1], 'x') as f:
                    pass
            case 'change_file0':
                with open(self.repo_path + '/' + self.filenames[0], 'a') as f:
                    f.write(get_random_garbage() + '\n')  # TODO also do changes to existing text
            case 'change_file1':
                with open(self.repo_path + '/' + self.filenames[1], 'a') as f:
                    f.write(get_random_garbage() + '\n')
            case 'delete_file0':
                os.remove(self.repo_path + '/' + self.filenames[0])
            case 'delete_file1':
                os.remove(self.repo_path + '/' + self.filenames[1])

            # Git commands
            case 'add_all':
                return self.repo.index.add(['.'])
            case 'add_file0':
                return self.repo.index.add([self.filenames[0]])  # Needs to be a list!
            case 'add_file1':
                return self.repo.index.add([self.filenames[1]])
            case 'commit':
                self.commit_number += 1
                return self.repo.index.commit("Commit number " + str(self.commit_number))
            case 'fetch':
                return self.repo.remotes['origin'].fetch()  # Alternative syntax: self.repo.remotes.origin.fetch()
            case 'tag':
                self.tag_number += 1
                return self.repo.create_tag('tag-' + str(self.tag_number))
            case _:
                if letter in input_alphabet:
                    raise RuntimeError("Something went terribly wrong!")
                else:
                    raise ValueError("This letter is not part of the alphabet!")


def main():
    # setup
    repo_path: str = '/tmp/repo'
    bare_repo_path: str = '/tmp/barerepo.git'
    assert not os.path.exists(repo_path)
    assert not os.path.exists(bare_repo_path)
    repo: Repo = Repo.init(repo_path)
    bare_repo: Repo = Repo.init(bare_repo_path, bare=True)
    assert not repo.bare
    assert bare_repo.bare
    # origin = repo.create_remote('origin', bare_repo_path)
    # assert origin.exists()
    # repo.create_head('master', origin.refs.master)  # create local branch "master" from remote "master"
    # repo.heads.master.set_tracking_branch(origin.refs.master)  # set local "master" to track remote "master
    # repo.heads.master.checkout()  # checkout local "master" to working tree

    # c'mon, do something
    assert not repo.is_dirty()
    with open(repo_path + '/' + 'file.txt', 'x') as f:
        pass
    repo.index.add(['file.txt'])
    assert repo.is_dirty()
    repo.index.commit("Add file.txt")

    assert not repo.is_dirty()
    with open(repo_path + '/' + 'file.txt', 'a') as f:
        f.write(get_random_garbage() + '\n')
    assert repo.is_dirty()
    print(repo.index.add(['file.txt']))
    print(repo.index.commit("Update file.txt"))

    # cleanup
    os.system('rm -rf ' + repo_path)
    os.system('rm -rf ' + bare_repo_path)


if __name__ == '__main__':
    main()

