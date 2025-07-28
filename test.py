import sys
sys.path.append('.')

from python_fsa.dfa import DFA

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

print(dfa.accepts((0, 1, 1, 0)))