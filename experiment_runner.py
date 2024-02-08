from aalpy.learning_algs import run_Lstar, run_KV
from aalpy.oracles import RandomWMethodEqOracle

from input_alphabets import *
from git_learning import GitSUL
from utils import *

# Paths to the repositories
repo_path: str = 'tmp/repo'
bare_repo_path: str = 'tmp/barerepo.git'

repo_path = os.path.abspath(repo_path)
bare_repo_path = os.path.abspath(bare_repo_path)

# ensures that tmp folders are empty
clean_up(None, repo_path, bare_repo_path)

for input_al_name, input_al in [('basic', basic_functionality_alphabet),
                                ('basic_with_remotes', basic_functionality_with_remote_alphabet),
                                ('extended', extended_functionality)]:
    for alg_name, learning_alg in [('L*', run_Lstar), ("KV", run_KV)]:

        print(f'{alg_name}_{input_al_name} --------------')
        git_sul = GitSUL(repo_path, bare_repo_path, mimic_cli_git_commit=False, verbose=False)
        eq_oracle = RandomWMethodEqOracle(input_al, git_sul, walks_per_state=10, walk_len=5)
        learned_model = run_Lstar(input_al, git_sul, eq_oracle, automaton_type='mealy')

        learned_model.save(f'models/{alg_name}_{input_al_name}')
        learned_model.visualize(path=f'models/{alg_name}_{input_al_name}.pdf')

        clean_up(git_sul.git, repo_path, bare_repo_path)
