"""Multiple-choice challenges ported 1:1 from the original challenges.js."""

CHALLENGES = [
    {
        "id": "QKD-01", "track": "QKD", "icon": "◈", "title": "Eve in the Middle",
        "difficulty": "Easy", "points": 100,
        "description": "Identify the attack from a BB84 session transcript.",
        "artifact": (
            "Alice bases:  + x + + x x + x + x\n"
            "Bob bases:    x x + + x + + x x x\n"
            "Sifted key QBER: 24.7%\n\n"
            "Observed behavior:\n"
            "Eve measures each photon in a randomly selected basis\n"
            "and resends a photon according to her result."
        ),
        "question": "Which attack best explains the observed disturbance?",
        "options": ["Photon loss", "Intercept-resend", "Classical denial of service", "Hash collision"],
        "answer": 1,
        "hint1": "The attacker measures before forwarding.",
        "hint2": "A basis mismatch between Eve and Alice introduces errors.",
        "explanation": "In BB84, intercept-resend causes errors because Eve does not know Alice's basis. Under full intercept-resend, the sifted-key QBER is approximately 25%.",
        "taxonomy": {"attack": "Quantum-enabled", "target": "QKD protocol", "tactic": "Interception", "objective": "Key compromise", "defense": "QBER monitoring"},
        "flag": "QKD{intercept_resend}",
    },
    {
        "id": "QKD-02", "track": "QKD", "icon": "◈", "title": "QBER Detector",
        "difficulty": "Easy", "points": 100,
        "description": "Act as the Blue Team and identify the compromised session.",
        "artifact": (
            "SESSION   QBER\n"
            "A         1.2%\n"
            "B         1.8%\n"
            "C        24.7%\n"
            "D         1.4%\n\n"
            "Baseline operational QBER: < 5%"
        ),
        "question": "Which session should the defender investigate first?",
        "options": ["A", "B", "C", "D"],
        "answer": 2,
        "hint1": "Look for the outlier.",
        "hint2": "A value near 25% is consistent with strong intercept-resend disturbance.",
        "explanation": "The defender should prioritize session C. A large QBER deviation is a security signal in QKD, although real systems require a full noise and implementation analysis.",
        "taxonomy": {"attack": "Detection", "target": "QKD session", "tactic": "Anomaly detection", "objective": "Eavesdropper identification", "defense": "QBER thresholding"},
        "flag": "QKD{qber_outlier_C}",
    },
    {
        "id": "PQC-01", "track": "PQC", "icon": "⌬", "title": "Quantum Safe?",
        "difficulty": "Easy", "points": 100,
        "description": "Classify primitives according to the quantum threat model.",
        "artifact": "RSA-2048\nECDSA-P256\nAES-256\nML-KEM-768\nML-DSA-65",
        "question": "Which pair is directly threatened by Shor's algorithm?",
        "options": ["AES-256 and ML-KEM-768", "RSA-2048 and ECDSA-P256", "ML-KEM-768 and ML-DSA-65", "AES-256 and RSA-2048"],
        "answer": 1,
        "hint1": "Think integer factorization and discrete logarithms.",
        "hint2": "Shor targets the mathematical structure behind RSA and ECC.",
        "explanation": "A sufficiently large fault-tolerant quantum computer running Shor's algorithm would break RSA and elliptic-curve cryptography. Symmetric cryptography has a different threat model, commonly associated with Grover-style search speedups.",
        "taxonomy": {"attack": "Quantum-enabled", "target": "Public-key cryptography", "tactic": "Shor", "objective": "Private-key recovery", "defense": "PQC migration"},
        "flag": "PQC{shor_targets_rsa_ecc}",
    },
    {
        "id": "PQC-02", "track": "PQC", "icon": "⌬", "title": "Algorithm Downgrade",
        "difficulty": "Medium", "points": 150,
        "description": "Find the protocol weakness that defeats a PQC migration.",
        "artifact": (
            "CLIENT\nsupported:\n  ML-KEM-768\n  ML-KEM-1024\n\n"
            "        v\n\nGATEWAY\nnegotiated:\n  RSA-2048\n\n"
            "        v\n\nSERVER\naccepted:\n  RSA-2048\n\n"
            "Policy:\n\"Prefer the strongest mutually supported\nquantum-resistant algorithm.\""
        ),
        "question": "What is the primary security failure?",
        "options": ["QBER spike", "Algorithm downgrade", "Nonce collision", "Quantum teleportation"],
        "answer": 1,
        "hint1": "The endpoint supports PQC, but the negotiated primitive is classical.",
        "hint2": "The attacker benefits when negotiation falls back to a weaker option.",
        "explanation": "PQC migration is not just an algorithm replacement. Protocol negotiation, policy enforcement, algorithm agility and downgrade resistance are part of the security boundary.",
        "taxonomy": {"attack": "Protocol", "target": "PQC migration", "tactic": "Downgrade", "objective": "Force classical primitive", "defense": "Downgrade-resistant negotiation"},
        "flag": "PQC{algorithm_downgrade}",
    },
    {
        "id": "QTM-01", "track": "Quantum Threats", "icon": "⚛", "title": "Quantum Trojan",
        "difficulty": "Medium", "points": 150,
        "description": "Inspect a circuit diff and identify the suspicious payload.",
        "svg": "assets/trojan.svg",
        "artifact": (
            "LEGITIMATE\nq0 --H----o----M\n          |\nq1 -------X----M\n\n"
            "MODIFIED\nq0 --H----o--------M\n          |\nq1 -------X----o----M\n"
            "               |\nq2 ------------X----\n\n"
            "Diff:\n+ q1 --o--\n       |\n+ q2 --X--"
        ),
        "question": "What is the most suspicious change?",
        "options": ["Removal of a measurement", "An additional controlled ancilla operation", "The Hadamard gate", "The first CNOT"],
        "answer": 1,
        "hint1": "Look at the newly introduced q2 interaction.",
        "hint2": "An unexpected controlled operation can act as a trigger or payload in an adversarial-circuit model.",
        "explanation": "This MVP models a quantum trojan as an intentionally inserted circuit modification. It is a research/educational abstraction, not a claim that this exact pattern is an established real-world malware technique.",
        "taxonomy": {"attack": "Adversarial circuit", "target": "Quantum program", "tactic": "Trojan insertion", "objective": "Hidden behavior", "defense": "Circuit integrity / attestation"},
        "flag": "QTM{ancilla_controlled_trojan}",
    },
    {
        "id": "QTM-02", "track": "Quantum Threats", "icon": "⚛", "title": "Malicious Circuit",
        "difficulty": "Hard", "points": 200,
        "description": "Identify the hidden trigger and payload in a circuit fragment.",
        "artifact": (
            "CONTROL FLOW\n\nif |secret_state> == |1>:\n    apply(payload)\n\n"
            "payload:\n    controlled operation\n    on ancilla q2\n\n"
            "Expected application:\n    f(x)\n\nObserved application:\n    f(x) + hidden side effect"
        ),
        "question": "Which security property is being violated?",
        "options": ["Availability only", "Program integrity / unauthorized behavior", "Classical password entropy", "QBER calibration"],
        "answer": 1,
        "hint1": "The circuit performs behavior outside the declared functional objective.",
        "hint2": "Think of a malicious modification that remains embedded in an otherwise valid quantum program.",
        "explanation": "The challenge models a malicious quantum circuit as unauthorized behavior hidden inside a legitimate computation. The useful security concepts are integrity, provenance, attestation, supply-chain controls and behavioral analysis.",
        "taxonomy": {"attack": "Quantum malware model", "target": "Quantum circuit", "tactic": "Hidden payload", "objective": "Unauthorized behavior", "defense": "Integrity / provenance / attestation"},
        "flag": "QTM{hidden_quantum_payload}",
    },
    {
        "id": "GROVER-01", "track": "Quantum Attacks", "icon": "∿", "title": "Grover Search Budget",
        "difficulty": "Hard", "points": 200,
        "description": "Determine the approximate number of Grover iterations for an unstructured search.",
        "artifact": "Search space:\nN = 16\n\nOracle marks one state.\n\nApproximate Grover iteration count:\nr ~ pi/4 x sqrt(N)",
        "question": "What is the closest integer to the recommended iteration count?",
        "options": ["1", "2", "3", "4"],
        "answer": 2,
        "hint1": "sqrt(16) = 4.",
        "hint2": "pi/4 x 4 ~ 3.14.",
        "explanation": "For a single marked item in a search space of N=16, the usual approximation gives about 3.14 Grover iterations, so 3 is the closest integer. This is an educational complexity challenge, not a claim of an operational attack against a deployed cryptosystem.",
        "taxonomy": {"attack": "Quantum algorithm", "target": "Unstructured search", "tactic": "Amplitude amplification", "objective": "Search speedup", "defense": "Quantum-aware security margin"},
        "flag": "GROVER{three_iterations}",
    },
    {
        "id": "GROVER-02", "track": "Quantum Attacks", "icon": "∿", "title": "Multiple Marked States",
        "difficulty": "Medium", "points": 150,
        "description": "Adjust the Grover iteration formula when more than one item is marked.",
        "artifact": "Search space:\nN = 64\nMarked states: M = 4\n\nWith multiple marked states:\nr ~ pi/4 x sqrt(N/M)",
        "question": "What is the closest integer to the recommended iteration count?",
        "options": ["2", "3", "6", "12"],
        "answer": 1,
        "hint1": "N/M = 64/4 = 16.",
        "hint2": "pi/4 x sqrt(16) = pi/4 x 4 ~ 3.14.",
        "explanation": "When multiple states are marked, the effective search space shrinks by a factor of M, so the iteration count uses sqrt(N/M) instead of sqrt(N). Here N/M = 16, giving roughly 3 iterations.",
        "taxonomy": {"attack": "Quantum algorithm", "target": "Unstructured search (multiple targets)", "tactic": "Amplitude amplification", "objective": "Search speedup", "defense": "Quantum-aware security margin"},
        "flag": "GROVER{multi_marked_three_iterations}",
    },
    {
        "id": "GROVER-03", "track": "Quantum Attacks", "icon": "∿", "title": "Symmetric Key Security Margin",
        "difficulty": "Hard", "points": 200,
        "description": "Determine the key-length mitigation needed against Grover's quadratic speedup.",
        "artifact": (
            "Cipher: AES-128\nClassical brute-force: 2^128 operations\n"
            "Grover-accelerated brute-force: ~ 2^64 operations\n\nTarget post-quantum security margin: 128 bits"
        ),
        "question": "Which symmetric key size restores a ~128-bit security margin against a quantum adversary using Grover's algorithm?",
        "options": ["AES-128 (no change needed)", "AES-192", "AES-256", "AES-512 (does not exist)"],
        "answer": 2,
        "hint1": "Grover roughly halves the effective security bits (quadratic speedup, not exponential).",
        "hint2": "128 x 2 = 256.",
        "explanation": "Grover's algorithm gives a quadratic speedup for brute-force key search, roughly halving a symmetric cipher's effective bit-security. Doubling the key length, e.g. migrating to AES-256, is the standard mitigation to restore a 128-bit post-quantum security margin.",
        "taxonomy": {"attack": "Quantum algorithm", "target": "Symmetric-key cryptography", "tactic": "Grover", "objective": "Brute-force key search speedup", "defense": "Key-length doubling"},
        "flag": "GROVER{aes256_migration}",
    },
    {
        "id": "GROVER-04", "track": "Quantum Attacks", "icon": "∿", "title": "Hash Preimage Search",
        "difficulty": "Medium", "points": 150,
        "description": "Compare classical vs Grover-accelerated preimage search against a cryptographic hash.",
        "artifact": (
            "Classical preimage search:        O(2^n)\n"
            "Grover-accelerated preimage search: O(2^(n/2))\n\nTarget: SHA-256 (n = 256 bits)"
        ),
        "question": "What is the approximate Grover-accelerated preimage-search complexity for SHA-256?",
        "options": ["2^256", "2^128", "2^64", "2^32"],
        "answer": 1,
        "hint1": "Apply the square-root speedup to the classical exponent.",
        "hint2": "256 / 2 = 128.",
        "explanation": "Grover's quadratic speedup reduces an n-bit hash's preimage resistance from 2^n to approximately 2^(n/2). For SHA-256 that is about 2^128 operations, unlike Shor's algorithm, which breaks RSA/ECC exponentially rather than just halving the exponent.",
        "taxonomy": {"attack": "Quantum algorithm", "target": "Hash function preimage resistance", "tactic": "Grover", "objective": "Search speedup against hashing", "defense": "Sufficient output length margin"},
        "flag": "GROVER{sha256_128bit_quantum_margin}",
    },
]

TRACK_DESCRIPTIONS = {
    "QKD": "Quantum Key Distribution",
    "PQC": "Post-Quantum Cryptography",
    "Quantum Threats": "Trojans, malicious circuits & quantum threat models",
    "Quantum Attacks": "Quantum attack algorithms",
    "Quantum Lab": "Hands-on Qiskit circuit-building challenges",
}
