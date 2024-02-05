from typing import Union

from aalpy.base import SUL
from aalpy.oracles import RandomWMethodEqOracle
from aalpy.learning_algs import run_Lstar

from git_handling import *
from utils import *
from input_alphabets import *

# Paths to the repositories
repo_path: str = 'tmp/repo'
bare_repo_path: str = 'tmp/barerepo.git'

repo_path = os.path.abspath(repo_path)
bare_repo_path = os.path.abspath(bare_repo_path)

# ensures that tmp folders are empty
clean_up(None, repo_path, bare_repo_path)


class GitSUL(SUL):
    def __init__(self, path_to_repo, path_to_remote, mimic_cli_git_commit=False, verbose=True):
        super().__init__()
        self.repo_path: str = path_to_repo
        self.bare_repo_path: str = path_to_remote
        assert not os.path.exists(self.repo_path)
        assert not os.path.exists(self.bare_repo_path)

        self.filenames: list[str] = ['file0.txt', 'file1.txt']

        self.branches = ['master', 'other_branch']

        self.git: Union[GitWrapper, None] = None
        self.mimic_cli_git_commit = mimic_cli_git_commit

        self.verbose = verbose

    def pre(self):
        self.git = GitWrapper(self.repo_path, self.bare_repo_path, self.mimic_cli_git_commit)

    def post(self):
        clean_up(self.git, repo_path, bare_repo_path)

    def query(self, word: tuple) -> list:
        outputs = super(GitSUL, self).query(word)
        if self.verbose:
            print(f'Current query and outputs: {list(zip(word, outputs))}')
        return outputs

    def step(self, letter):
        # File operations
        if letter == 'create_f0':
            return create_file(self.repo_path + '/' + self.filenames[0])
        elif letter == 'create_f1':
            return create_file(self.repo_path + '/' + self.filenames[1])
        elif letter == 'change_f0':
            return change_file(self.repo_path + '/' + self.filenames[0])
        elif letter == 'change_f1':
            return change_file(self.repo_path + '/' + self.filenames[1])
        elif letter == 'delete_f0':
            return delete_file(self.repo_path + '/' + self.filenames[0])
        elif letter == 'delete_f1':
            return delete_file(self.repo_path + '/' + self.filenames[0])

        # Git status checks
        elif letter == 'branch':
            return self.git.current_branch()
        elif letter == 'untracked':
            return self.git.untracked()
        elif letter == 'dirty':
            return self.git.is_dirty()
        elif letter == 'modified':
            return self.git.modified()

        # Git commands
        elif letter == 'add_all':
            return self.git.add('.')
        elif letter == 'add_f0':
            return self.git.add(self.filenames[0])
        elif letter == 'add_f1':
            return self.git.add(self.filenames[1])
        elif letter == 'commit':
            return self.git.commit()
        elif letter == 'tag':
            return self.git.tag()
        elif letter == 'fetch':
            return self.git.fetch()
        elif letter == 'pull':
            return self.git.pull()
        elif letter == 'push':
            return self.git.push()
        elif letter == 'create_branch':
            return self.git.create_branch(self.branches[1])
        elif letter == 'checkout_branch':
            return self.git.checkout(self.branches[1])
        elif letter == 'checkout_master':
            return self.git.checkout(self.branches[0])
        else:
            raise ValueError("This letter is not part of the alphabet! (Letter: " + letter + ")")


if __name__ == '__main__':
    input_alphabet = basic_functionality_with_remote_alphabet

    git_sul = GitSUL(repo_path, bare_repo_path, mimic_cli_git_commit=False)
    eq_oracle = RandomWMethodEqOracle(input_alphabet, git_sul, walks_per_state=20, walk_len=10)
    learned_model = run_Lstar(input_alphabet, git_sul, eq_oracle, automaton_type='mealy')

    learned_model.visualize(path='models/basic_functionality_with_remotes.pdf')
    learned_model.save('models/basic_functionality_with_remotes')

    clean_up(git_sul.git, repo_path, bare_repo_path)
