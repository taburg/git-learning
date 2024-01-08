from aalpy.base import Automaton


def print_automaton_details(mealy: Automaton):
    print("-"*35)
    print("Automaton has", len(mealy.states), "states")
    for state in mealy.states:
        print("  *", state.state_id)
        for i in state.transitions.keys():
            dst_state = state.transitions[i]
            o = state.output_fun[i]
            print(f" -> {dst_state.state_id} : {i} / {o}")
        print("")
    print("-"*35)


def explore_automaton_interactive(mealy: Automaton):
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


