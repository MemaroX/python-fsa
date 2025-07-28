# Python Finite State Automata (python-fsa): Unlocking the Power of Computation

## A Masterpiece of Automata Theory in Python

`python-fsa` transcends the ordinary, offering an exquisitely crafted Python library for the profound exploration, precise manipulation, and stunning visualization of Deterministic Finite Automata (DFAs) and Nondeterministic Finite Automata (NFAs). This isn't merely a collection of scripts; it's a meticulously engineered framework designed to empower engineers, researchers, and students to effortlessly define, analyze, and bring to life the very essence of computational logic.

## Unparalleled Capabilities

-   **DFA & NFA Implementation:** At its core, `python-fsa` provides elegantly designed classes that embody the mathematical rigor of finite automata. Simulate complex computational processes with unparalleled clarity and efficiency.
-   **Input Acceptance Testing:** Witness the computational prowess as the automata flawlessly determine the acceptance or rejection of input strings, providing instantaneous insights into language recognition.
-   **NFA to DFA Conversion:** Conquer the inherent complexities of nondeterminism with a seamless, mathematically sound conversion mechanism that transforms any NFA into its equivalent, deterministic counterpart, simplifying analysis without compromising power.
-   **Transducers:** Dive into the dynamic world of step-by-step computation. Our mutable transducers allow for granular processing of input symbols, revealing the intricate dance of state transitions in real-time.
-   **Interactive FSM Creation (`fsm_creator.py`):** Unleash your creativity with an intuitive command-line interface that transforms the abstract process of FSM definition into an engaging, guided experience. Effortlessly sculpt your automata, generating both human-readable JSON definitions and visually stunning DOT graph files.
-   **Advanced CLI (`main3-0.py`):** Command your automata with precision. This versatile interface empowers you to load FSMs from diverse sources – be it the structured elegance of JSON or the visual poetry of DOT graph files. Engage in interactive testing, including a mesmerizing step-by-step execution mode that illuminates every computational step.
-   **DOT File Customization (`dot_customizer.py`):** Elevate your visualizations to an art form. This utility grants you unprecedented control over the aesthetic presentation of your automata, allowing programmatic modification and rendering of DOT graph files for truly bespoke diagrams. Highlight critical states, emphasize transitions, and make your FSMs speak volumes.
-   **Visualization:** Beyond mere functionality, `python-fsa` integrates seamlessly with Graphviz, transforming abstract mathematical concepts into breathtaking visual diagrams (PNG). Witness the beauty of your computational designs unfold before your eyes.

## Installation: A Gateway to Computational Elegance

`python-fsa` leverages the power of `pygraphviz` for its stunning visualizations, which in turn requires the foundational Graphviz C library. To ensure a flawless installation, follow these steps, paving your way to computational mastery:

1.  **Install Graphviz:** Secure your foundation by installing Graphviz from the [official website](https://graphviz.org/download/). Crucially, ensure its `dot` executable is meticulously placed within your system's PATH for seamless integration.

2.  **Install Python Dependencies:** Arm your Python environment with the necessary components:

    ```bash
    pip install -r requirements.txt
    pip install graphviz
    ```

3.  **Install `python-fsa` in Editable Mode (for development/CLI tools):** Unlock the full potential of the project by installing it in editable mode, allowing real-time modifications and direct access to its powerful CLI tools:

    ```bash
    pip install -e .
    ```

## Usage: Orchestrating Your Automata

### Interactive FSM Creation (`fsm_creator.py`)

Embark on your FSM design journey with this guided interactive experience. Define your DFA or NFA with precision, and watch as it generates both a `.dot` file for visual splendor and a `.json` file for future programmatic endeavors.

```bash
python fsm_creator.py
```

Follow the intuitive prompts to sculpt your automaton. Upon completion, you'll be presented with the option to immediately launch `main3-0.py`, allowing you to instantly test the computational prowess of your newly forged FSM.

### Advanced FSM CLI (`main3-0.py`)

This is your command center for interacting with the very fabric of finite state machines. Load and test FSMs from a multitude of sources, including the meticulously crafted JSON files from `fsm_creator.py` or the visually expressive DOT graph files.

**Load from JSON and test:**

```bash
python main3-0.py --load-from my_fsm.json
```

**Load from DOT file and test:**

```bash
python main3-0.py --dot-file assets/dot_files/dfa_example.gv
```

Once within the interactive testing realm, you possess the power to input strings for immediate acceptance/rejection analysis or invoke the `step` command for a captivating, symbol-by-symbol execution, revealing the automaton's internal journey.

### DOT File Customization (`dot_customizer.py`)

Transform your FSM diagrams into works of art. This utility provides the granular control necessary to programmatically modify and render existing DOT graph files. For instance, to visually emphasize the initial state:

```bash
python dot_customizer.py --input assets/dot_files/dfa_example.gv --output customized_dfa
```

Behold as `customized_dfa.dot` and `customized_dfa.png` emerge, with the initial state now boldly highlighted in red, a testament to your command over visual representation.

### Library Usage (Examples)

For those who prefer direct programmatic interaction, `python-fsa` offers a clean and powerful API.

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

## Acknowledgements

This project stands on the shoulders of giants. We extend our profound gratitude to **James Ansley** (GitHub: [James-Ansley](https://github.com/James-Ansley)) for his foundational work on the original `python-fsa` repository, which served as the initial inspiration and starting point for this enhanced endeavor. His elegant design principles laid the groundwork for the advanced capabilities now present.
