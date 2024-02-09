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
                                ('basic_with_remotes', basic_functionality_with_remote_alphabet),
                                ('extended', extended_functionality)]:

    for alg_name, learning_alg in [('L_star_', run_Lstar), ('KV', run_KV)]:
        print(f'Comparing CMD and Gitpython on {input_al_name}')

        cmd_model = load_automaton_from_file(f'cmd_{alg_name}_{input_al_name}.dot', 'mealy')
        gitPython_model = load_automaton_from_file(f'gitPython_{alg_name}_{input_al_name}.dot', 'mealy')

        shortest_counterexample = bisimilar(cmd_model, gitPython_model)

        if shortest_counterexample:
            print(f'Shortest Counterexample: {shortest_counterexample}')
            print(f'CFM Interface           : {cmd_model.execute_sequence(cmd_model.initial_state, shortest_counterexample)}')
            print(f'GitPython Interface     : {gitPython_model.execute_sequence(cmd_model.initial_state, shortest_counterexample)}')

            more_cex = compare_automata(cmd_model, gitPython_model, num_cex=5)
            print('Additional counterexamples')
            for cex in more_cex:
                print(f'Counterexample        : {shortest_counterexample}')
                print(f'CFM Interface           : {cmd_model.execute_sequence(cmd_model.initial_state, shortest_counterexample)}')
                print(f'GitPython Interface     : {gitPython_model.execute_sequence(cmd_model.initial_state, shortest_counterexample)}')

        else:
            print("CMD and GitPython interfaces behave the same.")



