# Quantum Cyber Range — Streamlit Edition

A Quantum Cybersecurity micro-CTF: the original 10 multiple-choice challenges
(QKD, PQC, Quantum Threats, Quantum Attacks) plus a new **Quantum Lab** track
where participants build real quantum circuits gate-by-gate and get graded by
an actual Qiskit `Statevector` simulation — not a hardcoded answer key.

## ⚠️ Deployment note: this is NOT GitHub Pages compatible

GitHub Pages only serves static files (HTML/CSS/JS). This app runs a live
Python process, so it needs a Python-hosting platform instead. Use one of:

## Deploy for free — Streamlit Community Cloud (recommended)

1. Push this folder to a GitHub repo (e.g. `quantum-cyber-range-streamlit`).
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. Click **New app**, pick the repo, branch `main`, main file `app.py`.
4. Click **Deploy**. Live in ~2 minutes at
   `https://<something>.streamlit.app`.

Free tier note: the app sleeps after inactivity; the next visitor sees a
~30 second cold start while it wakes up.

## Deploy for free — Hugging Face Spaces (alternative)

1. Create a new Space, SDK = **Streamlit**.
2. Upload these files (or connect the GitHub repo).
3. Space builds automatically from `requirements.txt`.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## What's new vs. the static version

- **Quantum Lab** track (`LAB-01` to `LAB-03`): build a Bell pair, a GHZ
  state, and the |-> state by picking gates from a menu. The circuit is
  simulated with `qiskit.quantum_info.Statevector` and compared to the
  target state with `.equiv()` (state-equality up to global phase) — real
  physics, not string matching.
- Progress and score live in `st.session_state` (resets on browser refresh
  unless you add persistent storage — see "Next steps" below).

## Security note on the Quantum Lab design

Participants build circuits by selecting gates from a fixed menu rather than
submitting free-form Python. This keeps the publicly deployed app safe from
arbitrary code execution while still being backed by a real Qiskit
simulation for grading.

## Next steps (optional, not implemented to keep this shippable in 24h)

- Persist progress across sessions (e.g. a small SQLite file or a free
  Supabase/Firebase project) instead of `st.session_state`.
- Add a 4th Lab challenge using `qiskit-aer` for shot-based measurement
  (counts/histogram) instead of exact statevectors — heavier dependency,
  left out to keep the Community Cloud build fast.
- Deep-linkable challenge URLs via `st.query_params`.
