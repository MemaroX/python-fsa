import argparse
import sys
import os
from python_fsa import DFA, NFA
import graphviz

def visualize_automaton(automaton, automaton_type, filename="automaton_visualization"):
    dot = graphviz.Digraph(comment=f'{automaton_type.upper()} Visualization')
    dot.attr('node', shape='circle')
    dot.attr(rankdir='LR')

    # Add invisible start node and edge to initial state
    dot.node('start', shape='none', width='0', height='0')
    dot.edge('start', automaton.initial)

    # Add nodes
    for state in automaton.states:
        if state in automaton.final:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)

    # Add transitions
    if automaton_type == 'dfa':
        for (state, symbol), next_state in automaton.transitions.items():
            dot.edge(state, next_state, label=str(symbol))
    elif automaton_type == 'nfa':
        for (state, symbol), next_states in automaton.transitions.items():
            for next_state in next_states:
                dot.edge(state, next_state, label=str(symbol))

    output_path = f"{filename}.png"
    dot.render(filename, view=False, format='png', cleanup=True)
    print(f"Visualization saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Create and test a Finite State Automaton.")
    parser.add_argument('--type', choices=['dfa', 'nfa'], required=True, help="Type of automaton to create (dfa or nfa).")
    parser.add_argument('--alphabet', required=True, help="Comma-separated list of alphabet symbols (e.g., '0,1').")
    parser.add_argument('--states', required=True, help="Comma-separated list of state names (e.g., 'q0,q1,q2').")
    parser.add_argument('--initial', required=True, help="Name of the initial state.")
    parser.add_argument('--final', required=True, help="Comma-separated list of final state names.")
    parser.add_argument('--transitions', required=True, nargs='+', help="List of transitions, each in the format 'state,symbol,next_state' (e.g., q0,0,q1 q0,1,q2). For NFAs, you can specify multiple next states like 'q0,1,q0,q1'.")
    parser.add_argument('--output-file', help="Optional: Filename for the visualization (e.g., 'my_automaton'). Default is 'automaton_visualization'.")

    args = parser.parse_args()

    # --- Process Arguments ---
    alphabet = tuple(s.strip() for s in args.alphabet.split(','))
    states = tuple(s.strip() for s in args.states.split(','))
    initial = args.initial.strip()
    final_states = tuple(s.strip() for s in args.final.split(','))

    if initial not in states:
        print(f"Error: Initial state '{initial}' is not in the list of defined states: {states}")
        sys.exit(1)

    for state in final_states:
        if state not in states:
            print(f"Error: Final state '{state}' is not in the list of defined states: {states}")
            sys.exit(1)

    # --- Build Transition Table ---
    transitions = {}
    if args.type == 'dfa':
        for t in args.transitions:
            parts = tuple(s.strip() for s in t.split(','))
            if len(parts) != 3:
                print(f"Error: Invalid DFA transition format: '{t}'. Expected 'state,symbol,next_state'.")
                sys.exit(1)
            state, symbol, next_state = parts
            if state not in states:
                print(f"Error: Transition '{t}': State '{state}' is not defined in states: {states}")
                sys.exit(1)
            if symbol not in alphabet:
                print(f"Error: Transition '{t}': Symbol '{symbol}' is not defined in alphabet: {alphabet}")
                sys.exit(1)
            if next_state not in states:
                print(f"Error: Transition '{t}': Next state '{next_state}' is not defined in states: {states}")
                sys.exit(1)
            if (state, symbol) in transitions:
                print(f"Error: Duplicate DFA transition for ({state}, {symbol}). DFA transitions must be unique.")
                sys.exit(1)
            transitions[(state, symbol)] = next_state
    else: # NFA
        for t in args.transitions:
            parts = tuple(s.strip() for s in t.split(','))
            if len(parts) < 3:
                print(f"Error: Invalid NFA transition format: '{t}'. Expected 'state,symbol,next_state1,next_state2,...'.")
                sys.exit(1)
            state, symbol = parts[0], parts[1]
            next_states_for_transition = tuple(parts[2:])

            if state not in states:
                print(f"Error: Transition '{t}': State '{state}' is not defined in states: {states}")
                sys.exit(1)
            if symbol not in alphabet:
                print(f"Error: Transition '{t}': Symbol '{symbol}' is not defined in alphabet: {alphabet}")
                sys.exit(1)
            for ns in next_states_for_transition:
                if ns not in states:
                    print(f"Error: Transition '{t}': Next state '{ns}' is not defined in states: {states}")
                    sys.exit(1)
            
            if (state, symbol) in transitions:
                transitions[(state, symbol)] += next_states_for_transition
            else:
                transitions[(state, symbol)] = next_states_for_transition

    # --- Create Automaton ---
    automaton = None
    if args.type == 'dfa':
        automaton = DFA(
            alphabet=alphabet,
            states=states,
            initial=initial,
            final=final_states,
            transitions=transitions
        )
        print(f"\n{args.type.upper()} created successfully!")
    else:
        automaton = NFA(
            alphabet=alphabet,
            states=states,
            initial=initial,
            final=final_states,
            transitions=transitions
        )
        print(f"\n{args.type.upper()} created successfully!")

    # --- Visualization ---
    output_filename = args.output_file if args.output_file else f"{args.type}_visualization"
    visualize_automaton(automaton, args.type, output_filename)

    # --- Interactive Testing ---
    print("\n--- Interactive Testing ---")
    print(f"Enter strings over the alphabet {alphabet} (comma-separated for multi-character symbols, e.g., 'a,b,c').")
    print("Type 'exit' to quit.")
    while True:
        try:
            user_input = input("> ").strip()
            if user_input.lower() == 'exit':
                break
            if not user_input:
                continue
            
            input_symbols = tuple(user_input.split(',')) if ',' in user_input else tuple(user_input)

            # Validate input symbols against the automaton's alphabet
            invalid_symbols = [s for s in input_symbols if s not in alphabet]
            if invalid_symbols:
                print(f"Error: Input contains symbols not in the defined alphabet {alphabet}: {invalid_symbols}")
                continue

            if automaton.accepts(input_symbols):
                print("  -> Accepted")
            else:
                print("  -> Rejected")
        except (EOFError, KeyboardInterrupt):
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
    print("\nGoodbye!")


if __name__ == "__main__":
    main()
