from aalpy import RandomWMethodEqOracle
from aalpy.base import SUL
from aalpy.learning_algs import run_Lstar

from git_handling import *
from utils import *

# Paths to the repositories
repo_path: str = 'tmp/repo'
bare_repo_path: str = 'tmp/barerepo.git'

repo_path = os.path.abspath(repo_path)
bare_repo_path = os.path.abspath(bare_repo_path)

# ensures that tmp folders are empty
clean_up(None, repo_path, bare_repo_path)

# Comment these in/out to enable/disable them
input_alphabet: list = [
    # File operations
    'create_f0',  # Create a file
    'create_f1',
    'change_f0',  # Apply changes to a file
    'change_f1',
    'delete_f0',  # Delete a file
    'delete_f1',

    # Git status checks
    # They do not/should not change state
    # 'branch',  # Reveal the current branch
    # 'untracked',  # Reveal the number of untracked files
    # 'dirty',  # Reveal whether something was added, but not committed yet
    # 'modified',  # Reveal the modified files

    # Git commands
    'add_all',  # Add files
    'add_f0',
    'add_f1',
    'commit',  # Make a commit
    'fetch',  # Fetch from remote
    'pull',  # Pull from remote
    'push',  # Push to remote, implies --set-remote for new branches
    'tag',  # Create a tag
    'create_branch',  # Create a new branch
    'checkout_branch',  # Checkout the newly created branch
    'checkout_master'  # Checkout master
]

reduced_input_alphabet: list = [
    # File operations
    'create_f0',  # Create a file
    'change_f0',  # Apply changes to a file
    'delete_f0',  # Delete a file

    # Git commands
    'add_f0',
    'commit',  # Make a commit
    'pull',  # Pull from remote
    'push',  # Push to remote, implies --set-remote for new branches
]


class GitSUL(SUL):
    def __init__(self, path_to_repo, path_to_remote, mimic_cli_git_commit=False):
        super().__init__()
        self.repo_path: str = path_to_repo
        self.bare_repo_path: str = path_to_remote
        assert not os.path.exists(self.repo_path)
        assert not os.path.exists(self.bare_repo_path)

        self.filenames: list[str] = ['file0.txt', 'file1.txt']

        self.branches = ['master', 'other_branch']

        self.git: GitWrapper | None = None
        self.mimic_cli_git_commit = mimic_cli_git_commit

    def pre(self):
        self.git = GitWrapper(self.repo_path, self.bare_repo_path, self.mimic_cli_git_commit)

    def post(self):
        clean_up(self.git, repo_path, bare_repo_path)

    def query(self, word: tuple) -> list:
        print(f'Current query: {word}')
        return super(GitSUL, self).query(word)

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


use_reduced_alphabet = True
input_alphabet = input_alphabet if not use_reduced_alphabet else reduced_input_alphabet

git_sul = GitSUL(repo_path, bare_repo_path, mimic_cli_git_commit=False)
eq_oracle = RandomWMethodEqOracle(input_alphabet, git_sul, walks_per_state=20, walk_len=10)
learned_model = run_Lstar(input_alphabet, git_sul, eq_oracle, automaton_type='mealy')

# learned_model = run_KV(input_alphabet, git_sul, eq_oracle, automaton_type='learned_model', cache_and_non_det_check=True)

learned_model.visualize(path='git-model.pdf')
print(learned_model)
learned_model.save('git-model')

clean_up(git_sul.git, repo_path, bare_repo_path)

# # Second version, imitating the behaviour of command line commit
# git_sul_2 = GitSUL(repo_path, bare_repo_path, mimic_cli_git_commit=True)
# eq_oracle_2 = RandomWordEqOracle(input_alphabet, git_sul, num_walks=500, min_walk_len=5, max_walk_len=20)
# learned_model_2 = run_Lstar(input_alphabet, git_sul_2, eq_oracle_2, automaton_type='mealy', cache_and_non_det_check=True)
# # learned_model_2 = run_KV(input_alphabet, git_sul, eq_oracle, automaton_type='mealy', cache_and_non_det_check=True)
#
# learned_model_2.visualize(path='git-model_2.pdf')
# print(learned_model_2)
# learned_model_2.save('git-model_2')
#
# clean_up(repo_path, bare_repo_path)
#
# # Compare the two automata
# diffs = compare_automata(learned_model, learned_model_2)
#
