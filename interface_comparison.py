from aalpy.learning_algs import run_Lstar, run_KV
from aalpy.utils import load_automaton_from_file
from aalpy.utils.ModelChecking import bisimilar, compare_automata

from input_alphabets import *
from utils import *

# Paths to the repositories
repo_path: str = 'tmp/repo'
bare_repo_path: str = 'tmp/barerepo.git'

repo_path = os.path.abspath(repo_path)
bare_repo_path = os.path.abspath(bare_repo_path)

# ensures that tmp folders are empty
clean_up(None, repo_path, bare_repo_path)

for input_al_name, input_al in [('basic', basic_functionality_alphabet),
                                ('basic_with_remotes', remotes_alphabet),
                                ('basics_with_remotes_and_branches', extended_functionality)]:

    for alg_name, learning_alg in [('L_star', run_Lstar),]:
            for allow_empty in [True, False]:

                print(f'Comparing CMD and Gitpython on {input_al_name}, allow empty {allow_empty}')

                cmd_model = load_automaton_from_file(f'models/cmd_empty_{allow_empty}_{input_al_name}_{alg_name}.dot', 'mealy')
                gitPython_model = load_automaton_from_file(f'models/gitPython_empty_{allow_empty}_{input_al_name}_{alg_name}.dot', 'mealy')

                shortest_counterexample = bisimilar(cmd_model, gitPython_model,return_cex=True)

                if shortest_counterexample:
                    print(f'Shortest Counterexample: {shortest_counterexample}')
                    print(f'CFM Interface           : {cmd_model.execute_sequence(cmd_model.initial_state, shortest_counterexample)}')
                    print(f'GitPython Interface     : {gitPython_model.execute_sequence(gitPython_model.initial_state, shortest_counterexample)}')

                    more_cex = compare_automata(cmd_model, gitPython_model, num_cex=5)
                    print('Additional counterexamples')
                    for cex in more_cex:
                        print(f'Counterexample        : {cex}')
                        print(f'CFM Interface           : {cmd_model.execute_sequence(cmd_model.initial_state, cex)}')
                        print(f'GitPython Interface     : {gitPython_model.execute_sequence(gitPython_model.initial_state, cex)}')

                else:
                    print("CMD and GitPython interfaces behave the same.")



