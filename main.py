import os
import random

import aalpy
import git
from aalpy.base import SUL
from aalpy.oracles import RandomWalkEqOracle, WMethodEqOracle
from aalpy.learning_algs import run_Lstar, run_KV
from aalpy.utils import visualize_automaton
from git import Repo, Remote

from filehandling import *
from githandling import *
from explorer import print_automaton_details

repo_path: str = '/tmp/repo'
bare_repo_path: str = '/tmp/barerepo.git'

input_alphabet: list = [
    # File operations
    'create_f0',
    # 'create_f1',
    'change_f0',
    # 'change_f1',
    'delete_f0',
    # 'delete_f1',

    # Git status checks
    # 'untracked',
    # 'dirty',

    # Git commands
    # 'add_all',
    'add_f0',
    # 'add_f1',
    'commit',
    # 'fetch',
    # 'pull',
    # 'push',
    # 'tag'
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

        self.filenames: list[str] = ['file0.txt', 'file1.txt']

        self.git: GitWrapper | None = None

    def pre(self):
        self.git = GitWrapper(self.repo_path, self.bare_repo_path)

    def post(self):
        if self.git is not None:
            self.git.destroy()  # Important, do not forget!
        self.git = None

    def step(self, letter):
        match letter:
            # File operations
            case 'create_f0':
                return create_file(self.repo_path + '/' + self.filenames[0])
            case 'create_f1':
                return create_file(self.repo_path + '/' + self.filenames[1])
            case 'change_f0':
                return change_file(self.repo_path + '/' + self.filenames[0])
            case 'change_f1':
                return change_file(self.repo_path + '/' + self.filenames[1])
            case 'delete_f0':
                return delete_file(self.repo_path + '/' + self.filenames[0])
            case 'delete_f1':
                return delete_file(self.repo_path + '/' + self.filenames[0])

            # Git status checks
            case 'untracked':
                return self.git.untracked()
            case 'dirty':
                return self.git.is_dirty()

            # Git commands
            case 'add_all':
                return self.git.add('.')
            case 'add_f0':
                return self.git.add(self.filenames[0])
            case 'add_f1':
                return self.git.add(self.filenames[1])
            case 'commit':
                return self.git.commit()
            # case 'fetch':
            #     return self.repo.remotes['origin'].fetch()  # Alternative syntax: self.repo.remotes.origin.fetch()
            case 'tag':
                return self.git.tag()
            case _:
                if letter in input_alphabet:
                    raise RuntimeError("Something went terribly wrong! (Letter: " + letter + ")")
                else:
                    raise ValueError("This letter is not part of the alphabet! (Letter: " + letter + ")")


def main():
    global input_alphabet
    global repo_path
    global bare_repo_path

    git_sul = GitSUL(repo_path, bare_repo_path)
    eq_oracle = RandomWalkEqOracle(input_alphabet, git_sul)
    mealy = run_Lstar(input_alphabet, git_sul, eq_oracle, automaton_type='mealy', cache_and_non_det_check=True)
    # mealy = run_KV(input_alphabet, git_sul, eq_oracle, automaton_type='mealy', cache_and_non_det_check=True)

    visualize_automaton(mealy, 'git-model.pdf')
    print_automaton_details(mealy)


if __name__ == '__main__':
    main()
