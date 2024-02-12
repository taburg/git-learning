from aalpy.utils import load_automaton_from_file
from aalpy.utils.ModelChecking import bisimilar, compare_automata

from input_alphabets import *

for input_al_name, input_al in [('basic', basic_functionality_alphabet),
                                ('basic_with_remotes', remotes_alphabet),
                                ('basics_with_remotes_and_branches', extended_functionality)]:

    for alg_name in ['L_star']:
            for allow_empty in [True, False]:

                print('---------------------------------------------------------------------------------------------------------------------------------')
                print(f'Comparing CMD and Gitpython on {input_al_name}, allow empty {allow_empty}')

                cmd_model = load_automaton_from_file(f'models/cmd_empty_{allow_empty}_{input_al_name}_{alg_name}.dot', 'mealy')
                gitPython_model = load_automaton_from_file(f'models/gitPython_empty_{allow_empty}_{input_al_name}_{alg_name}.dot', 'mealy')

                shortest_counterexample = bisimilar(cmd_model, gitPython_model, return_cex=True)

                if shortest_counterexample:
                    print(f'Shortest Counterexample: {shortest_counterexample}')
                    print(f'CMD Interface           : {cmd_model.execute_sequence(cmd_model.initial_state, shortest_counterexample)}')
                    print(f'GitPython Interface     : {gitPython_model.execute_sequence(gitPython_model.initial_state, shortest_counterexample)}')

                    more_cex = compare_automata(cmd_model, gitPython_model, num_cex=20)
                    print('Additional counterexamples')
                    for cex in more_cex:
                        print(f'Counterexample        :   {cex}')
                        print(f'CMD Interface           : {cmd_model.execute_sequence(cmd_model.initial_state, cex)}')
                        print(f'GitPython Interface     : {gitPython_model.execute_sequence(gitPython_model.initial_state, cex)}')

                else:
                    print("CMD and GitPython interfaces behave the same.")

#
# if __name__ == '__main__':
#     from aalpy.learning_algs import run_Lstar
#     from aalpy.oracles import RandomWMethodEqOracle
#     from GitCmdSUL import GitCmdSUL
#     from GitPythonSUL import GitPythonSUL
#     from input_alphabets import *
#
#     from utils import *
#
#     # Paths to the repositories
#     repo_path: str = 'tmp/repo'
#     bare_repo_path: str = 'tmp/barerepo.git'
#
#     # ensures that tmp folders are empty
#     clean_up(None, repo_path, bare_repo_path)
#
#     # If you want to use CMD interface to git set to True, for GitPython set to False
#     use_cmd_git = True
#     # Allow empty commit
#     allow_emtpy_commit = True
#
#     git_sul_cmd = GitCmdSUL(repo_path, bare_repo_path, allow_empty_commit=allow_emtpy_commit)
#     git_sul_python = GitPythonSUL(repo_path, bare_repo_path, allow_empty_commit=allow_emtpy_commit)
#
#     #quee = ('create_f0', 'add_f0', 'delete_f0', 'commit', 'create_branch', 'checkout_branch', 'delete_f0')
#     quee = ('create_f0', 'commit', 'add_f0', 'create_branch', 'commit', 'checkout_branch', 'create_f0', 'checkout_master')
#     cmd = git_sul_cmd.query(quee)
#     print(cmd)
#
#     pyt = git_sul_python.query(quee)
#     print(pyt)