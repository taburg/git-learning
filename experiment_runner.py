from aalpy.learning_algs import run_Lstar, run_KV
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

for alg_name, learning_alg in [('L_star', run_Lstar), ('KV', run_KV)]:

    for input_al_name, input_al in [('basic', basic_functionality_alphabet),
                                    ('basic_with_remotes', remotes_alphabet),]:
                                    #('basics_with_remotes_and_branches', remotes_branching_alphabet), ]:

        for interface_type, sul in [('cmd', GitCmdSUL), ('gitPython', GitPythonSUL)]:
            for allow_empty in [True, False]:
                print(f'{alg_name}_{input_al_name}_{interface_type}_empty_{allow_empty}--------------')
                git_sul = sul(repo_path, bare_repo_path, allow_empty_commit=allow_empty, verbose=False)

                eq_oracle = RandomWMethodEqOracle(input_al, git_sul, walks_per_state=25, walk_len=10)
                learned_model = run_Lstar(input_al, git_sul, eq_oracle, automaton_type='mealy')

                learned_model.save(f'models/{interface_type}_empty_{allow_empty}_{input_al_name}_{alg_name}')

                clean_up(None if interface_type == 'cmd' else git_sul.git, repo_path, bare_repo_path)
