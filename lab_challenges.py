"""
Quantum Lab: hands-on circuit-building challenges powered by Qiskit.

Design note: instead of executing arbitrary user-submitted Python (exec),
the participant builds a circuit by picking gates from a fixed, safe menu.
The resulting circuit is simulated with Qiskit's Statevector and compared
to a target state with .equiv() (state-equality up to global phase).
This keeps the app safe to deploy publicly while still being a real,
Qiskit-backed hands-on exercise instead of another multiple-choice quiz.
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

GATE_MENU = ["H", "X", "Z", "CX"]  # Hadamard, Pauli-X, Pauli-Z, CNOT


def build_circuit(n_qubits: int, ops: list[tuple]) -> QuantumCircuit:
    """ops: list of (gate:str, qubit:int) or ('CX', control:int, target:int)."""
    qc = QuantumCircuit(n_qubits)
    for op in ops:
        gate = op[0]
        if gate == "H":
            qc.h(op[1])
        elif gate == "X":
            qc.x(op[1])
        elif gate == "Z":
            qc.z(op[1])
        elif gate == "CX":
            qc.cx(op[1], op[2])
    return qc


def target_bell(n_qubits=2) -> QuantumCircuit:
    qc = QuantumCircuit(n_qubits)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def target_ghz(n_qubits=3) -> QuantumCircuit:
    qc = QuantumCircuit(n_qubits)
    qc.h(0)
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)
    return qc


def target_minus(n_qubits=1) -> QuantumCircuit:
    qc = QuantumCircuit(n_qubits)
    qc.x(0)
    qc.h(0)
    return qc


LAB_CHALLENGES = [
    {
        "id": "LAB-01",
        "title": "Build a Bell Pair",
        "difficulty": "Easy",
        "points": 150,
        "n_qubits": 2,
        "goal": (
            "Entangle two qubits into the Bell state (|00> + |11>) / sqrt(2). "
            "This is the building block behind QKD protocols like E91."
        ),
        "target_fn": target_bell,
        "hint1": "Start with a Hadamard on qubit 0 to create superposition.",
        "hint2": "Then apply CX with qubit 0 as control and qubit 1 as target.",
        "flag": "LAB{bell_state_entangled}",
    },
    {
        "id": "LAB-02",
        "title": "Build a GHZ State",
        "difficulty": "Medium",
        "points": 200,
        "n_qubits": 3,
        "goal": (
            "Entangle three qubits into the GHZ state (|000> + |111>) / sqrt(2), "
            "used to reason about multi-party quantum correlations."
        ),
        "target_fn": target_ghz,
        "hint1": "Same start as a Bell pair: Hadamard on qubit 0.",
        "hint2": "Chain CX gates: (0,1) then (1,2) to spread the entanglement.",
        "flag": "LAB{ghz_state_three_qubits}",
    },
    {
        "id": "LAB-03",
        "title": "Prepare the |-> State",
        "difficulty": "Easy",
        "points": 100,
        "n_qubits": 1,
        "goal": (
            "Prepare the single-qubit state |-> = (|0> - |1>) / sqrt(2), "
            "the eigenstate BB84 uses in the diagonal basis."
        ),
        "target_fn": target_minus,
        "hint1": "Flip the qubit to |1> first with X.",
        "hint2": "Then apply H to rotate into the diagonal basis.",
        "flag": "LAB{minus_state_diagonal_basis}",
    },
]


def check_solution(qc: QuantumCircuit, target_fn) -> bool:
    n = qc.num_qubits
    sv_user = Statevector.from_instruction(qc)
    sv_target = Statevector.from_instruction(target_fn(n))
    return sv_user.equiv(sv_target)
