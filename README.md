# Python Finite State Automata (python-fsa)

`python-fsa` is a Python library designed for the creation, manipulation, and visualization of Deterministic Finite Automata (DFAs) and Nondeterministic Finite Automata (NFAs). It provides a robust framework for defining state machines, processing input strings, and generating visual representations of the automata.

## Features

-   **DFA & NFA Implementation:** Core classes for defining and simulating both deterministic and nondeterministic finite automata.
-   **Input Acceptance Testing:** Methods to check if a given input string is accepted by the defined automaton.
-   **NFA to DFA Conversion:** Functionality to convert NFA instances into equivalent DFA representations.
-   **Transducers:** Mutable transducers for step-by-step processing of input symbols.
-   **Interactive FSM Creation (`fsm_creator.py`):** A command-line tool to guide users through the interactive definition of DFAs and NFAs, generating both JSON and DOT graph files.
-   **Advanced CLI (`main3-0.py`):** A versatile command-line interface for loading FSMs from JSON or DOT files, performing interactive testing (including step-by-step execution), and generating visualizations.
-   **DOT File Customization (`dot_customizer.py`):** A utility to programmatically modify and render DOT graph files, allowing for visual enhancements (e.g., highlighting initial states).
-   **Visualization:** Integration with Graphviz to generate visual diagrams (PNG) of the created automata.

## Installation

`python-fsa` depends on `pygraphviz` for visualization, which in turn requires the Graphviz C library to be installed on your system. If you encounter issues with `pygraphviz` installation, ensure Graphviz is properly installed and its `dot` executable is in your system's PATH.

1.  **Install Graphviz:** Download and install Graphviz from the [official website](https://graphviz.org/download/) and ensure it's added to your system's PATH.

2.  **Install Python Dependencies:**

    ```bash
    pip install -r requirements.txt
    pip install graphviz
    ```

3.  **Install `python-fsa` in Editable Mode (for development/CLI tools):**

    ```bash
    pip install -e .
    ```

## Usage

### Interactive FSM Creation (`fsm_creator.py`)

This tool guides you through defining a new DFA or NFA interactively. It generates a `.dot` file for visualization and a `.json` file for programmatic use.

```bash
python fsm_creator.py
```

Follow the prompts to define your automaton. At the end, you'll have the option to launch `main3-0.py` to immediately test your newly created FSM.

### Advanced FSM CLI (`main3-0.py`)

This script allows you to load and test FSMs from various sources, including JSON files (created by `fsm_creator.py`) or DOT graph files.

**Load from JSON and test:**

```bash
python main3-0.py --load-from my_fsm.json
```

**Load from DOT file and test:**

```bash
python main3-0.py --dot-file assets/dot_files/dfa_example.gv
```

Once in interactive mode, you can enter strings to test or type `step` for step-by-step execution.

### DOT File Customization (`dot_customizer.py`)

Modify and render existing DOT graph files. For example, to highlight the initial state:

```bash
python dot_customizer.py --input assets/dot_files/dfa_example.gv --output customized_dfa
```

This will create `customized_dfa.dot` and `customized_dfa.png` with the initial state colored red.

### Library Usage (Examples)

**DFA Example:**

```python
from python_fsa import DFA

a, b = "a", "b"

dfa = DFA(
    alphabet=(0, 1),
    states=(a, b),
    initial=a,
    transitions={
        (a, 0): a,
        (a, 1): b,
        (b, 0): b,
        (b, 1): a,
    },
    final=(a,),
)

print(dfa.accepts((0, 1, 1, 0)))  # Output: True
print(dfa.accepts((0, 0, 0, 1)))  # Output: False
```

**NFA Example:**

```python
from python_fsa import NFA

a, b, c = "a", "b", "c"

nfa = NFA(
    alphabet=(0, 1),
    states=(a, b, c),
    initial=a,
    transitions={
        (a, 0): (a,),
        (a, 1): (a, b),
        (b, 0): (c,),
        (b, 1): (c,),
    },
    final=(c,),
)

print(nfa.accepts((0, 1, 1, 0)))  # Output: True
print(nfa.accepts((0, 0, 0, 1)))  # Output: False

# Convert NFA to DFA
dfa_from_nfa = nfa.to_dfa()
print(dfa_from_nfa.accepts((0, 1, 1, 0))) # Output: True
```