import os
import random

import aalpy
import git
from aalpy.base import SUL
from aalpy.oracles import RandomWalkEqOracle
from aalpy.learning_algs import run_Lstar
from aalpy.utils import visualize_automaton
from git import Repo, Remote

repo_path: str = '/tmp/repo'
bare_repo_path: str = '/tmp/barerepo.git'

input_alphabet: list = [
    # File operations
    'create_file0',
    # 'create_file1',
    'change_file0',
    # 'change_file1',
    'delete_file0',
    # 'delete_file1',

    # Git pseudo-commands and status checks
    # 'list_untracked_files',
    'is_dirty',

    # Git commands
    # 'add_all',
    'add_file0',
    # 'add_file1',
    'commit',
    # 'fetch',
    # 'pull',
    # 'push',
    'tag'
]


def print_repo_data(repo: Repo):
    reader = repo.config_reader()
    for section in reader.sections():
        print("+++", section, "+++")
        print(reader.items_all(section))
    print("----- ----- -----")


def get_random_garbage() -> str:
    return str(random.choices(range(ord('A'), ord('Z')), k=random.randint(5, 25)))


class GitSUL(SUL):
    def __init__(self, path_to_repo, path_to_bare_repo):
        super().__init__()
        self.repo_path: str = path_to_repo
        self.bare_repo_path: str = path_to_bare_repo
        assert not os.path.exists(self.repo_path)
        assert not os.path.exists(self.bare_repo_path)
        self.repo: Repo | None = None
        self.bare_repo: Repo | None = None

        self.filenames: list = ['file0.txt', 'file1.txt']
        self.commit_number: int = -1
        self.tag_number: int = -1

    def __del__(self):
        try:
            os.system('rm -rf ' + self.repo_path)
        except FileNotFoundError:
            pass
        try:
            os.system('rm -rf ' + self.bare_repo_path)
        except FileNotFoundError:
            pass

    def pre(self):
        self.repo = Repo.init(self.repo_path)
        self.bare_repo = Repo.init(self.bare_repo_path, bare=True)
        assert not self.repo.bare
        assert self.bare_repo.bare
        # self.repo.create_remote('origin', self.bare_repo_path)
        self.commit_number = -1
        self.tag_number = -1

    def post(self):
        os.system('rm -rf ' + self.repo_path)
        os.system('rm -rf ' + self.bare_repo_path)
        self.repo = None
        self.bare_repo = None

    def step(self, letter):
        match letter:
            # File operations
            case 'create_file0':
                try:
                    with open(self.repo_path + '/' + self.filenames[0], 'x') as f:
                        pass
                    return "CREATE_SUCCESS " + self.filenames[0]
                except Exception:
                    return "CREATE_FAIL " + self.filenames[0]
            case 'create_file1':
                try:
                    with open(self.repo_path + '/' + self.filenames[1], 'x') as f:
                        pass
                    return "CREATE_SUCCESS " + self.filenames[1]
                except Exception:
                    return "CREATE_FAIL " + self.filenames[1]
            case 'change_file0':
                try:
                    with open(self.repo_path + '/' + self.filenames[0], 'a') as f:
                        f.write(get_random_garbage() + '\n')  # TODO also do changes to existing text
                    return "WRITE_SUCCESS " + self.filenames[0]
                except Exception:
                    return "WRITE_FAIL " + self.filenames[0]
            case 'change_file1':
                try:
                    with open(self.repo_path + '/' + self.filenames[1], 'a') as f:
                        f.write(get_random_garbage() + '\n')  # TODO also do changes to existing text
                    return "WRITE_SUCCESS " + self.filenames[1]
                except Exception:
                    return "WRITE_FAIL " + self.filenames[1]
            case 'delete_file0':
                try:
                    os.remove(self.repo_path + '/' + self.filenames[0])
                    return "DELETE_SUCCESS " + self.filenames[0]
                except Exception:
                    return "DELETE_FAIL " + self.filenames[0]
            case 'delete_file1':
                try:
                    os.remove(self.repo_path + '/' + self.filenames[1])
                    return "DELETE_SUCCESS " + self.filenames[1]
                except Exception:
                    return "DELETE_FAIL " + self.filenames[1]

            # Git commands
            case 'list_untracked_files':
                return "UNTRACKED " + str(self.repo.untracked_files)
            case 'is_dirty':
                return "REPO_DIRTY" if self.repo.is_dirty() else "REPO_NOT_DIRTY"
            case 'add_all':
                try:
                    self.repo.index.add(['.'])
                    return "ADD_SUCCESS"
                except Exception:
                    return "ADD_FAIL"
            case 'add_file0':
                try:
                    self.repo.index.add([self.filenames[0]])  # Needs to be a list!
                    return "ADD_SUCCESS"
                except Exception:
                    return "ADD_FAIL"
            case 'add_file1':
                try:
                    self.repo.index.add([self.filenames[1]])
                    return "ADD_SUCCESS"
                except Exception:
                    return "ADD_FAIL"
            case 'commit':
                try:
                    self.commit_number += 1
                    self.repo.index.commit("Commit number " + str(self.commit_number))
                    return "COMMIT_SUCCESS"
                except Exception:
                    return "COMMIT_FAIL"
            # case 'fetch':
            #     return self.repo.remotes['origin'].fetch()  # Alternative syntax: self.repo.remotes.origin.fetch()
            case 'tag':
                try:
                    self.tag_number += 1
                    return "TAG " + str(self.repo.create_tag('tag-' + str(self.tag_number)))
                except Exception:
                    return "TAG_FAIL"
            case _:
                if letter in input_alphabet:
                    print(letter)
                    raise RuntimeError("Something went terribly wrong!")
                else:
                    raise ValueError("This letter is not part of the alphabet!")


def testing():
    # setup
    global repo_path
    global bare_repo_path
    assert not os.path.exists(repo_path)
    assert not os.path.exists(bare_repo_path)

    repo: Repo = Repo.init(repo_path)
    bare_repo: Repo = Repo.init(bare_repo_path, bare=True)
    assert not repo.bare
    assert bare_repo.bare

    # debug prints
    print_repo_data(repo)
    print_repo_data(bare_repo)

    print(repo.active_branch)
    print(repo.head)

    origin: Remote = repo.create_remote('origin', url=bare_repo_path)
    assert origin.exists()

    # c'mon, do something
    assert not repo.is_dirty()
    with open(repo_path + '/' + 'file.txt', 'x') as f:
        pass
    repo.index.add(['file.txt'])
    assert repo.is_dirty()
    repo.index.commit("Add file.txt")

    # origin.push(refspec="master:origin")

    assert not repo.is_dirty()
    with open(repo_path + '/' + 'file.txt', 'a') as f:
        f.write(get_random_garbage() + '\n')
    assert repo.is_dirty()
    repo.index.add(['file.txt'])
    repo.index.commit("Update file.txt")

    # cleanup
    os.system('rm -rf ' + repo_path)
    os.system('rm -rf ' + bare_repo_path)


def main():
    global input_alphabet
    global repo_path
    global bare_repo_path

    git_sul = GitSUL(repo_path, bare_repo_path)
    eq_oracle = RandomWalkEqOracle(input_alphabet, git_sul, num_steps=100)
    mealy = run_Lstar(input_alphabet, git_sul, eq_oracle, automaton_type='mealy', cache_and_non_det_check=True)

    visualize_automaton(mealy)


if __name__ == '__main__':
    main()
