from aalpy.base import Automaton


def explore_automaton(mealy: Automaton):
    while True:
        command = input('> ').split()
        match command[0]:
            case "count":
                print(len(mealy.states), "States")
            case "states":
                for state in mealy.states:
                    print(state.state_id)
            case "transitions":
                state = mealy.get_state_by_id(command[1])
                for i in state.transitions.keys():
                    dst_state = state.transitions[i]
                    o = state.output_fun[i]
                    print(f" -> {dst_state.state_id} : {i} / {o}")
            case "help":
                print("Available commands:\n"
                      "  count\n"
                      "  states\n"
                      "  transitions\n"
                      "  help\n"
                      "  quit")
            case "quit":
                return


