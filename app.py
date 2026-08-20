import streamlit as st
from qiskit import QuantumCircuit

from challenges_data import CHALLENGES, TRACK_DESCRIPTIONS
from lab_challenges import LAB_CHALLENGES, GATE_MENU, build_circuit, check_solution

st.set_page_config(
    page_title="Quantum Cyber Range",
    page_icon="assets/favicon.png",
    layout="wide",
)

# ---------- state ----------
if "solved" not in st.session_state:
    st.session_state.solved = {}
if "score" not in st.session_state:
    st.session_state.score = 0
if "lab_ops" not in st.session_state:
    st.session_state.lab_ops = {c["id"]: [] for c in LAB_CHALLENGES}

ALL_IDS = [c["id"] for c in CHALLENGES] + [c["id"] for c in LAB_CHALLENGES]
TOTAL = len(ALL_IDS)


def mark_solved(cid, points):
    if cid not in st.session_state.solved:
        st.session_state.solved[cid] = True
        st.session_state.score += points


# ---------- minimal CSS to echo the original dark theme ----------
st.markdown(
    """
    <style>
    .flag-box{display:inline-block;padding:6px 10px;border-radius:8px;
      background:#06130f;color:#57d49a;font-family:ui-monospace,monospace;font-weight:700;}
    .tax-table td{padding:2px 8px;font-size:14px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- sidebar / navigation ----------
st.sidebar.markdown("## ⚛ Quantum Cyber Range")
st.sidebar.metric("Score", f"{st.session_state.score} pts")
st.sidebar.progress(len(st.session_state.solved) / TOTAL)
st.sidebar.caption(f"{len(st.session_state.solved)}/{TOTAL} solved")

if st.sidebar.button("Reset progress"):
    st.session_state.solved = {}
    st.session_state.score = 0
    st.session_state.lab_ops = {c["id"]: [] for c in LAB_CHALLENGES}
    st.rerun()

tracks = list(dict.fromkeys([c["track"] for c in CHALLENGES])) + ["Quantum Lab"]
page = st.sidebar.radio("Track", ["Home"] + tracks)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Educational MVP. MCQ flags are for learning purposes; Quantum Lab "
    "challenges are validated by real Qiskit simulation."
)


# ---------- MCQ challenge renderer ----------
def render_mcq(c):
    already = c["id"] in st.session_state.solved
    st.markdown(f"#### {c['id']} · {c['title']}  <span style='color:#f4c96b;font-size:14px'>· {c['difficulty']} · {c['points']} pts</span>", unsafe_allow_html=True)
    st.caption(c["description"])

    if c.get("svg"):
        st.image(c["svg"], use_container_width=True)

    st.code(c["artifact"], language=None)

    st.markdown(f"**{c['question']}**")
    choice = st.radio("Answer", c["options"], key=f"radio-{c['id']}", label_visibility="collapsed")
    idx = c["options"].index(choice)

    col1, col2 = st.columns([1, 4])
    with col1:
        submit = st.button("Review" if already else "Submit", key=f"submit-{c['id']}")
    with col2:
        if already:
            st.caption("Already solved — no extra points for resubmitting.")

    if submit:
        if idx == c["answer"]:
            mark_solved(c["id"], c["points"])
            st.success(c["explanation"])
            st.markdown(f"<span class='flag-box'>{c['flag']}</span>", unsafe_allow_html=True)
        else:
            st.error("Not quite. Re-read the artifact and threat model. Use the hints if needed.")

    with st.expander("Hint 1"):
        st.write(c["hint1"])
    with st.expander("Hint 2"):
        st.write(c["hint2"])

    with st.expander("Threat model"):
        t = c["taxonomy"]
        st.markdown(
            f"""
            <table class="tax-table">
            <tr><td><b>Attack</b></td><td>{t['attack']}</td></tr>
            <tr><td><b>Target</b></td><td>{t['target']}</td></tr>
            <tr><td><b>Tactic</b></td><td>{t['tactic']}</td></tr>
            <tr><td><b>Objective</b></td><td>{t['objective']}</td></tr>
            <tr><td><b>Defense</b></td><td>{t['defense']}</td></tr>
            </table>
            """,
            unsafe_allow_html=True,
        )
    st.divider()


# ---------- Quantum Lab renderer ----------
def render_lab(c):
    already = c["id"] in st.session_state.solved
    st.markdown(f"#### {c['id']} · {c['title']}  <span style='color:#f4c96b;font-size:14px'>· {c['difficulty']} · {c['points']} pts</span>", unsafe_allow_html=True)
    st.caption(c["goal"])

    n = c["n_qubits"]
    ops_key = c["id"]
    ops = st.session_state.lab_ops[ops_key]

    st.markdown("**Build your circuit** — add gates in order, then simulate.")
    gcol1, gcol2, gcol3 = st.columns([2, 2, 1])
    with gcol1:
        gate = st.selectbox("Gate", GATE_MENU, key=f"gate-{c['id']}")
    with gcol2:
        if gate == "CX":
            qa, qb = st.columns(2)
            control = qa.selectbox("Control qubit", list(range(n)), key=f"ctrl-{c['id']}")
            target = qb.selectbox("Target qubit", list(range(n)), key=f"targ-{c['id']}")
        else:
            qubit = st.selectbox("Qubit", list(range(n)), key=f"q-{c['id']}")
    with gcol3:
        st.write("")
        st.write("")
        if st.button("Add gate", key=f"add-{c['id']}"):
            if gate == "CX":
                if control == target:
                    st.warning("Control and target must differ.")
                else:
                    ops.append(("CX", control, target))
            else:
                ops.append((gate, qubit))

    bcol1, bcol2 = st.columns([1, 1])
    with bcol1:
        if st.button("Undo last gate", key=f"undo-{c['id']}") and ops:
            ops.pop()
    with bcol2:
        if st.button("Clear circuit", key=f"clear-{c['id']}"):
            ops.clear()

    qc = build_circuit(n, ops)
    st.code(str(qc.draw(output="text")), language=None)

    if st.button("Run simulation & check", key=f"run-{c['id']}", type="primary"):
        if check_solution(qc, c["target_fn"]):
            mark_solved(c["id"], c["points"])
            st.success("Correct state prepared! Statevector matches the target (up to global phase).")
            st.markdown(f"<span class='flag-box'>{c['flag']}</span>", unsafe_allow_html=True)
        else:
            from qiskit.quantum_info import Statevector
            probs = Statevector.from_instruction(qc).probabilities_dict()
            st.error("Not the target state yet.")
            st.caption(f"Current measurement probabilities: {probs}")

    if already:
        st.caption("✓ Already solved.")

    with st.expander("Hint 1"):
        st.write(c["hint1"])
    with st.expander("Hint 2"):
        st.write(c["hint2"])
    st.divider()


# ---------- pages ----------
if page == "Home":
    st.title("Quantum Cyber Range")
    st.write(
        "A Streamlit-powered Quantum Cybersecurity micro-CTF covering QKD, "
        "post-quantum cryptography, quantum attacks, adversarial circuits — "
        "plus a hands-on **Quantum Lab** built with real Qiskit simulation."
    )
    m1, m2, m3 = st.columns(3)
    m1.metric("Score", f"{st.session_state.score} pts")
    m2.metric("Solved", f"{len(st.session_state.solved)}/{TOTAL}")
    m3.metric("Tracks", len(tracks))

    for t in tracks:
        items = [c for c in CHALLENGES if c["track"] == t] if t != "Quantum Lab" else LAB_CHALLENGES
        solved_n = sum(1 for c in items if c["id"] in st.session_state.solved)
        st.markdown(f"**{t}** — {TRACK_DESCRIPTIONS.get(t, '')}  ·  {solved_n}/{len(items)} solved")
        st.progress(solved_n / len(items) if items else 0)

elif page == "Quantum Lab":
    st.title("⚛ Quantum Lab")
    st.caption(
        "Build real quantum circuits gate-by-gate. Every circuit is simulated with "
        "Qiskit's Statevector — no fake grading, the physics is real."
    )
    for c in LAB_CHALLENGES:
        render_lab(c)

else:
    st.title(page)
    st.caption(TRACK_DESCRIPTIONS.get(page, ""))
    for c in [c for c in CHALLENGES if c["track"] == page]:
        render_mcq(c)
