from aalpy.learning_algs import run_Lstar
from aalpy.oracles import RandomWMethodEqOracle
from aalpy.utils import compare_automata
from GitCmdSUL import GitCmdSUL
from GitPythonSUL import GitPythonSUL
from input_alphabets import *

from utils import *

# Paths to the repositories
repo_path: str = 'tmp/repo'
bare_repo_path: str = 'tmp/barerepo.git'

repo_path = os.path.abspath(repo_path)
bare_repo_path = os.path.abspath(bare_repo_path)

# ensures that tmp folders are empty
clean_up(None, repo_path, bare_repo_path)

# select which input alphabet to use
input_alphabet = basic_functionality_alphabet
# If you want to use CMD interface to git set to True, for GitPython set to False

learned_models = []
for use_cmd_git in [True, False]:
    if use_cmd_git:
        git_sul = GitCmdSUL(repo_path, bare_repo_path)
        interface_type = 'cmd'
    else:
        git_sul = GitPythonSUL(repo_path, bare_repo_path)
        interface_type = 'gitPython'

    eq_oracle = RandomWMethodEqOracle(input_alphabet, git_sul, walks_per_state=25, walk_len=10)
    learned_model = run_Lstar(input_alphabet, git_sul, eq_oracle, automaton_type='mealy')

    learned_model.visualize(path=f'models/{interface_type}_basic_functionality_with_remotes.pdf')
    learned_model.save(f'models/{interface_type}_basic_functionality_with_remotes')

    clean_up(None if interface_type == 'cmd' else git_sul.git, repo_path, bare_repo_path)

    learned_models.append(learned_model)

diffs = compare_automata(learned_models[0], learned_models[1], 50)
for d in diffs:
    print(d)
    out1 = learned_models[0].execute_sequence(learned_models[0].initial_state, d)
    print(out1)
    out2 = learned_models[1].execute_sequence(learned_models[1].initial_state, d)
    print(out2)
