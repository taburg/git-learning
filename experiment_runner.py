from aalpy.learning_algs import run_Lstar, run_KV
from aalpy.oracles import RandomWMethodEqOracle

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

for interface_type, sul in [('cmd', GitCmdSUL), ('gitPython', GitPythonSUL)]:
    for input_al_name, input_al in [('basic', basic_functionality_alphabet),
                                    ('basic_with_remotes', basic_functionality_with_remote_alphabet),
                                    ('extended', extended_functionality)]:
        for alg_name, learning_alg in [('L*', run_Lstar), ("KV", run_KV)]:
            print(f'{alg_name}_{input_al_name} --------------')
            git_sul = sul(repo_path, bare_repo_path, verbose=False)

            eq_oracle = RandomWMethodEqOracle(input_al, git_sul, walks_per_state=25, walk_len=10)
            learned_model = run_Lstar(input_al, git_sul, eq_oracle, automaton_type='mealy')

            learned_model.save(f'models/{interface_type}_{alg_name}_{input_al_name}')
            learned_model.visualize(path=f'models/{interface_type}_{alg_name}_{input_al_name}.pdf')

            clean_up(git_sul.git, repo_path, bare_repo_path)
