import argparse
import sys
from python_fsa import DFA, NFA
import graphviz

def main():
    parser = argparse.ArgumentParser(description="Create and test a Finite State Automaton.")
    parser.add_argument('--type', choices=['dfa', 'nfa'], required=True, help="Type of automaton to create (dfa or nfa).")
    parser.add_argument('--alphabet', required=True, help="Comma-separated list of alphabet symbols (e.g., '0,1').")
    parser.add_argument('--states', required=True, help="Comma-separated list of state names (e.g., 'q0,q1,q2').")
    parser.add_argument('--initial', required=True, help="Name of the initial state.")
    parser.add_argument('--final', required=True, help="Comma-separated list of final state names.")
    parser.add_argument('--transitions', required=True, nargs='+', help="List of transitions, each in the format 'state,symbol,next_state' (e.g., q0,0,q1 q0,1,q2). For NFAs, you can specify multiple next states like 'q0,1,q0,q1'.")

    args = parser.parse_args()

    alphabet = tuple(args.alphabet.split(','))
    states = tuple(args.states.split(','))
    initial = args.initial
    final_states = tuple(args.final.split(','))

    if initial not in states:
        print(f"Error: Initial state '{initial}' is not in the list of states.")
        sys.exit(1)

    for state in final_states:
        if state not in states:
            print(f"Error: Final state '{state}' is not in the list of states.")
            sys.exit(1)

    transitions = {}
    if args.type == 'dfa':
        for t in args.transitions:
            parts = t.split(',')
            if len(parts) != 3:
                print(f"Error: Invalid DFA transition format: '{t}'. Expected 'state,symbol,next_state'.")
                sys.exit(1)
            state, symbol, next_state = parts
            if state not in states or next_state not in states or symbol not in alphabet:
                 print(f"Error: Invalid transition '{t}'. Make sure all states and symbols are defined.")
                 sys.exit(1)
            transitions[(state, symbol)] = next_state
    else: # NFA
        for t in args.transitions:
            parts = t.split(',')
            if len(parts) < 3:
                print(f"Error: Invalid NFA transition format: '{t}'. Expected 'state,symbol,next_state1,next_state2,...'.")
                sys.exit(1)
            state, symbol = parts[0], parts[1]
            next_states = tuple(parts[2:])
            if state not in states or symbol not in alphabet:
                 print(f"Error: Invalid transition '{t}'. Make sure the state and symbol are defined.")
                 sys.exit(1)
            for ns in next_states:
                if ns not in states:
                    print(f"Error: Invalid next state '{ns}' in transition '{t}'.")
                    sys.exit(1)
            transitions[(state, symbol)] = next_states

    automaton = None
    if args.type == 'dfa':
        automaton = DFA(
            alphabet=alphabet,
            states=states,
            initial=initial,
            final=final_states,
            transitions=transitions
        )
        print("\nDFA created successfully!")

        # --- Visualization ---
        dot = graphviz.Digraph()
        dot.attr('node', shape='circle')
        dot.attr(rankdir='LR')

        # Add nodes
        for state in automaton.states:
            if state in automaton.final:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)

        # Add invisible start node
        dot.node('', shape='none', width='0', height='0')
        dot.edge('', automaton.initial)

        # Add transitions
        for (state, symbol), next_state in automaton.transitions.items():
            dot.edge(state, next_state, label=symbol)

        dot.render('dfa', view=False, format='png')
        print("DFA visualization saved to dfa.png")

    else:
        automaton = NFA(
            alphabet=alphabet,
            states=states,
            initial=initial,
            final=final_states,
            transitions=transitions
        )
        print("\nNFA created successfully!")

    print("Enter strings to test (one per line). Type 'exit' to quit.")
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == 'exit':
                break
            
            input_symbols = tuple(user_input.split(',')) if ',' in user_input else tuple(user_input)

            if not all(s in alphabet for s in input_symbols):
                print(f"Error: Input contains symbols not in the defined alphabet {alphabet}")
                continue

            if automaton.accepts(input_symbols):
                print("  -> Accepted")
            else:
                print("  -> Rejected")
        except (EOFError, KeyboardInterrupt):
            break
    print("\nGoodbye!")


if __name__ == "__main__":
    main()