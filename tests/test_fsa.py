import pytest
from python_fsa import DFA, NFA

# Test cases for DFA
def test_dfa_accepts_even_ones():
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
    assert dfa.accepts((0, 0, 0, 1, 1)) == True  # Even number of 1s
    assert dfa.accepts((0, 1, 0, 1, 0)) == True  # Even number of 1s
    assert dfa.accepts((1, 1, 1, 1)) == True     # Even number of 1s
    assert dfa.accepts((0, 0, 0, 1)) == False    # Odd number of 1s
    assert dfa.accepts((1, 0, 1, 1)) == False    # Odd number of 1s
    assert dfa.accepts(()) == True              # Empty string, 0 ones (even)

def test_dfa_transducer():
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
    transducer = dfa.transducer()
    assert transducer.current == a
    assert transducer.is_accepting == True
    transducer.push(1)
    assert transducer.current == b
    assert transducer.is_accepting == False
    transducer.push(1)
    assert transducer.current == a
    assert transducer.is_accepting == True

# Test cases for NFA
def test_nfa_accepts_second_to_last_one():
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
    assert nfa.accepts((0, 1, 1, 0)) == True
    assert nfa.accepts((0, 0, 0, 1)) == False
    assert nfa.accepts((1, 1)) == True
    assert nfa.accepts((0, 0)) == False
    assert nfa.accepts((1,)) == False
    assert nfa.accepts(()) == False

def test_nfa_to_dfa():
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
    dfa_from_nfa = nfa.to_dfa()

    # Test some strings with the converted DFA
    assert dfa_from_nfa.accepts((0, 1, 1, 0)) == True
    assert dfa_from_nfa.accepts((0, 0, 0, 1)) == False
    assert dfa_from_nfa.accepts((1, 1)) == True
    assert dfa_from_nfa.accepts((0, 0)) == False
    assert dfa_from_nfa.accepts((1,)) == False
    assert dfa_from_nfa.accepts(()) == False

    # Test squash method
    squashed_dfa = dfa_from_nfa.squash()
    assert squashed_dfa.accepts((0, 1, 1, 0)) == True
    assert squashed_dfa.accepts((0, 0, 0, 1)) == False

