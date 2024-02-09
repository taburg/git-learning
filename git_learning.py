from aalpy.learning_algs import run_Lstar
from aalpy.oracles import RandomWMethodEqOracle
from GitCmdSUL import GitCmdSUL
from GitPythonSUL import GitPythonSUL
from input_alphabets import *

from utils import *

# Paths to the repositories
repo_path: str = 'tmp/repo'
bare_repo_path: str = 'tmp/barerepo.git'

# ensures that tmp folders are empty
clean_up(None, repo_path, bare_repo_path)

# select which input alphabet to use
input_alphabet = remotes_alphabet
# If you want to use CMD interface to git set to True, for GitPython set to False
use_cmd_git = True
# Allow empty commit
allow_emtpy_commit = False

if use_cmd_git:
    git_sul = GitCmdSUL(repo_path, bare_repo_path, allow_empty_commit=allow_emtpy_commit)
    interface_type = 'cmd'
else:
    git_sul = GitPythonSUL(repo_path, bare_repo_path, allow_empty_commit=allow_emtpy_commit)
    interface_type = 'gitPython'


eq_oracle = RandomWMethodEqOracle(input_alphabet, git_sul, walks_per_state=25, walk_len=10)
learned_model = run_Lstar(input_alphabet, git_sul, eq_oracle, automaton_type='mealy', max_learning_rounds=4)

learned_model.visualize(path=f'models/{interface_type}_basic_functionality_with_remotes.pdf')
learned_model.save(f'models/{interface_type}_basic_functionality_with_remotes')

clean_up(None if interface_type == 'cmd' else git_sul.git, repo_path, bare_repo_path)
