import subprocess
import os
import pytest

# Define a temporary directory for test outputs
@pytest.fixture
def temp_output_dir(tmp_path):
    return tmp_path

def test_dfa_creation_and_visualization(temp_output_dir):
    output_filename = temp_output_dir / "test_dfa_viz"
    command = [
        "python",
        "main2-0.py",
        "--type", "dfa",
        "--alphabet", "0,1",
        "--states", "q0,q1",
        "--initial", "q0",
        "--final", "q1",
        "--transitions", "q0,0,q0", "q0,1,q1", "q1,0,q1", "q1,1,q0",
        "--output-file", str(output_filename)
    ]
    
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True, cwd=os.getcwd())

    # Assert that the command ran successfully
    assert result.returncode == 0, f"CLI command failed with error: {result.stderr}"
    assert "DFA created successfully!" in result.stdout
    assert f"Visualization saved to {output_filename}.png" in result.stdout

    # Assert that the output file was created
    assert os.path.exists(f"{output_filename}.png")

def test_nfa_creation_and_visualization(temp_output_dir):
    output_filename = temp_output_dir / "test_nfa_viz"
    command = [
        "python",
        "main2-0.py",
        "--type", "nfa",
        "--alphabet", "a,b",
        "--states", "s0,s1,s2",
        "--initial", "s0",
        "--final", "s2",
        "--transitions", "s0,a,s1", "s1,b,s2", "s0,a,s0",
        "--output-file", str(output_filename)
    ]
    
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True, cwd=os.getcwd())

    # Assert that the command ran successfully
    assert result.returncode == 0, f"CLI command failed with error: {result.stderr}"
    assert "NFA created successfully!" in result.stdout
    assert f"Visualization saved to {output_filename}.png" in result.stdout

    # Assert that the output file was created
    assert os.path.exists(f"{output_filename}.png")

def test_save_and_load_automaton(temp_output_dir):
    json_file = temp_output_dir / "test_automaton.json"
    output_filename = temp_output_dir / "loaded_dfa_viz"

    # 1. Create a DFA and save it
    create_command = [
        "python",
        "main2-0.py",
        "--type", "dfa",
        "--alphabet", "0,1",
        "--states", "q0,q1",
        "--initial", "q0",
        "--final", "q1",
        "--transitions", "q0,0,q0", "q0,1,q1", "q1,0,q1", "q1,1,q0",
        "--save-to", str(json_file),
        "--skip-visualization" # Skip visualization during creation
    ]
    result_create = subprocess.run(create_command, capture_output=True, text=True, cwd=os.getcwd())
    assert result_create.returncode == 0, f"Create command failed: {result_create.stderr}"
    assert os.path.exists(json_file)
    assert "Automaton saved to" in result_create.stdout

    # 2. Load the saved automaton and visualize it
    load_command = [
        "python",
        "main2-0.py",
        "--load-from", str(json_file),
        "--output-file", str(output_filename)
    ]
    result_load = subprocess.run(load_command, capture_output=True, text=True, cwd=os.getcwd())
    assert result_load.returncode == 0, f"Load command failed: {result_load.stderr}"
    assert "Automaton loaded successfully" in result_load.stdout
    assert f"Visualization saved to {output_filename}.png" in result_load.stdout
    assert os.path.exists(f"{output_filename}.png")

def test_invalid_input_error_handling():
    command = [
        "python",
        "main2-0.py",
        "--type", "dfa",
        "--alphabet", "0,1",
        "--states", "q0,q1",
        "--initial", "q0",
        "--final", "q1",
        "--transitions", "q0,0,q2" # q2 is not a defined state
    ]
    result = subprocess.run(command, capture_output=True, text=True, cwd=os.getcwd())
    assert result.returncode != 0 # Expect a non-zero exit code for error
    assert "Error: Transition 'q0,0,q2': Next state 'q2' is not defined in states: ('q0', 'q1')" in result.stderr

