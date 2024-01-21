import os
import random

import aalpy
from aalpy.base import SUL
from aalpy.oracles import RandomWordEqOracle, RandomWalkEqOracle, WMethodEqOracle
from aalpy.learning_algs import run_Lstar, run_KV
from aalpy.utils import visualize_automaton, compare_automata

from filehandling import *
from githandling import *
from explorer import print_automaton_details, log_automaton_details

# Paths to the repositories
repo_path: str = '/tmp/repo'
bare_repo_path: str = '/tmp/barerepo.git'

# Comment these in/out to enable/disable them
input_alphabet: list = [
    # File operations
    'create_f0',        # Create a file
    # 'create_f1',
    'change_f0',        # Apply changes to a file
    # 'change_f1',
    'delete_f0',        # Delete a file
    # 'delete_f1',

    # Git status checks
    # 'branch',           # Reveal the current branch
    # 'untracked',        # Reveal the number of untracked files
    # 'dirty',            # Reveal whether something was added, but not committed yet
    # 'modified',         # Reveal the modified files

    # Git commands
    # 'add_all',          # Add files
    'add_f0',
    # 'add_f1',
    'commit',           # Make a commit
    'fetch',            # Fetch from remote
    'pull',             # Pull from remote
    'push',             # Push to remote, implies --set-upstream for new branches
    'tag',              # Create a tag
    'create_branch',    # Create a new branch
    'checkout_branch',  # Checkout the newly created branch
    'checkout_master'   # Checkout master
]


def print_repo_data(repo: Repo):
    reader = repo.config_reader()
    for section in reader.sections():
        print("+++", section, "+++")
        print(reader.items_all(section))
    print("----- ----- -----")


def get_random_garbage() -> str:
    return str(random.choices(range(ord('A'), ord('Z')), k=random.randint(5, 25)))


def clean_up():
    if os.path.exists(repo_path):
        os.system('rm -rf ' + repo_path)
    if os.path.exists(bare_repo_path):
        os.system('rm -rf ' + bare_repo_path)


class GitSUL(SUL):
    def __init__(self, path_to_repo, path_to_bare_repo, mimic_cli_git_commit=False):
        super().__init__()
        self.repo_path: str = path_to_repo
        self.bare_repo_path: str = path_to_bare_repo
        assert not os.path.exists(self.repo_path)
        assert not os.path.exists(self.bare_repo_path)

        self.filenames: list[str] = ['file0.txt', 'file1.txt']

        self.branches = ['master', 'other_branch']

        self.git: GitWrapper | None = None
        self.mimic_cli_git_commit = mimic_cli_git_commit

    def pre(self):
        self.git = GitWrapper(self.repo_path, self.bare_repo_path, self.mimic_cli_git_commit)

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
            case 'branch':
                return self.git.current_branch()
            case 'untracked':
                return self.git.untracked()
            case 'dirty':
                return self.git.is_dirty()
            case 'modified':
                return self.git.modified()

            # Git commands
            case 'add_all':
                return self.git.add('.')
            case 'add_f0':
                return self.git.add(self.filenames[0])
            case 'add_f1':
                return self.git.add(self.filenames[1])
            case 'commit':
                return self.git.commit()
            case 'tag':
                return self.git.tag()
            case 'fetch':
                return self.git.fetch()
            case 'pull':
                return self.git.pull()
            case 'push':
                return self.git.push()
            case 'create_branch':
                return self.git.create_branch(self.branches[1])
            case 'checkout_branch':
                return self.git.checkout(self.branches[1])
            case 'checkout_master':
                return self.git.checkout(self.branches[0])
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
    eq_oracle = RandomWordEqOracle(input_alphabet, git_sul, num_walks=500)
    mealy = run_Lstar(input_alphabet, git_sul, eq_oracle, automaton_type='mealy', cache_and_non_det_check=True)
    # mealy = run_KV(input_alphabet, git_sul, eq_oracle, automaton_type='mealy', cache_and_non_det_check=True)

    visualize_automaton(mealy, 'git-model.pdf')
    print_automaton_details(mealy)
    log_automaton_details(mealy, 'git-model.log')

    clean_up()

    # # Second version, imitating the behaviour of command line commit
    # git_sul_2 = GitSUL(repo_path, bare_repo_path, True)
    # eq_oracle_2 = RandomWordEqOracle(input_alphabet, git_sul_2, num_walks=500)
    # mealy_2 = run_Lstar(input_alphabet, git_sul_2, eq_oracle_2, automaton_type='mealy', cache_and_non_det_check=True)
    # # mealy = run_KV(input_alphabet, git_sul, eq_oracle, automaton_type='mealy', cache_and_non_det_check=True)
    #
    # visualize_automaton(mealy_2, 'git-model-2.pdf')
    # print_automaton_details(mealy_2)
    # log_automaton_details(mealy_2, 'git-model-2.log')
    #
    # clean_up()
    #
    # # Compare the two automata
    # diffs = compare_automata(mealy, mealy_2)
    # print(diffs)


if __name__ == '__main__':
    main()
