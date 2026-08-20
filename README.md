# Quantum Cyber Range

A hands-on Quantum Cybersecurity micro-CTF (Capture The Flag). Ten multiple-choice
challenges across four threat tracks, plus **Quantum Lab**: three exercises where
participants build real quantum circuits and get graded by an actual
[Qiskit](https://www.ibm.com/quantum/qiskit) simulation — not a hardcoded answer key.

---

## Contents

- [Overview](#overview)
- [Tracks & challenges](#tracks--challenges)
- [How grading works](#how-grading-works)
- [Project structure](#project-structure)
- [Run locally](#run-locally)
- [Deploy for free](#deploy-for-free)
- [Troubleshooting](#troubleshooting)
- [Security design notes](#security-design-notes)
- [Roadmap](#roadmap)
- [License](#license)

## Overview

| | |
|---|---|
| **Format** | Single-page Streamlit app, no login, no database |
| **Challenges** | 10 multiple-choice + 3 hands-on Qiskit circuit builds |
| **State** | In-memory via `st.session_state` (resets on refresh — see [Roadmap](#roadmap)) |
| **Dependencies** | `streamlit`, `qiskit` — nothing else |
| **Cost to run** | $0 on Streamlit Community Cloud or Hugging Face Spaces |

## Tracks & challenges

| Track | Focus | Challenges |
|---|---|---|
| **QKD** | Quantum Key Distribution | Eve in the Middle, QBER Detector |
| **PQC** | Post-Quantum Cryptography | Quantum Safe?, Algorithm Downgrade |
| **Quantum Threats** | Adversarial / malicious circuits | Quantum Trojan, Malicious Circuit |
| **Quantum Attacks** | Quantum algorithm complexity | Grover Search Budget, Multiple Marked States, Symmetric Key Security Margin, Hash Preimage Search |
| **Quantum Lab** | Hands-on circuit building | Build a Bell Pair, Build a GHZ State, Prepare the \|−⟩ State |

## How grading works

**MCQ tracks (QKD, PQC, Quantum Threats, Quantum Attacks):** the selected option
is compared against a fixed answer key, same as a typical CTF quiz.

**Quantum Lab:** the participant builds a circuit by picking gates from a fixed
menu (H, X, Z, CX). No free-form code is executed. The resulting circuit is
simulated with `qiskit.quantum_info.Statevector` and compared to the target
state using `.equiv()` — state-vector equality up to global phase. This means
the grading is real quantum-state math, not string or code matching.

## Project structure

```
quantum-cyber-range-streamlit/
├── app.py                  # Streamlit UI, routing, rendering
├── challenges_data.py      # The 10 MCQ challenges (data only)
├── lab_challenges.py       # Quantum Lab targets + Qiskit grading logic
├── requirements.txt        # streamlit + qiskit, pinned
├── assets/
│   ├── favicon.png
│   └── trojan.svg          # Circuit diagram for the Quantum Trojan challenge
└── .streamlit/
    └── config.toml          # Dark theme matching the original static design
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`.

## Deploy for free

### Streamlit Community Cloud (recommended)

1. Push this folder to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. **New app** → pick the repo → branch `main` → main file `app.py`.
4. In **Advanced settings**, explicitly select a Python version (**3.11 or
   3.12** — see [Troubleshooting](#troubleshooting) for why this matters with Qiskit).
5. **Deploy**. Live in ~2 minutes at `https://<your-app>.streamlit.app`.

Free-tier note: the app sleeps after inactivity; the next visitor sees a
~30 second cold start.

### Hugging Face Spaces (alternative)

1. Create a new Space, SDK = **Streamlit**.
2. Connect this GitHub repo, or upload the files directly.
3. The Space builds automatically from `requirements.txt`.

> ⚠️ **Not GitHub Pages compatible.** GitHub Pages only serves static files.
> This app runs a live Python process and needs one of the platforms above.

## Troubleshooting

### `Segmentation fault` on Streamlit Cloud when using `qiskit>=2.0`

Qiskit ≥2.0 depends on `rustworkx`, a compiled Rust extension that only ships
prebuilt wheels for specific Python versions. Streamlit Community Cloud has a
[known, currently open issue](https://github.com/streamlit/streamlit/issues/15326)
where `runtime.txt` is ignored and the build silently runs on a newer Python
than expected. When that happens, pip resolves to a `rustworkx`/Qiskit wheel
that doesn't match the actual interpreter ABI, and the process segfaults on
import instead of failing with a normal error.

**Fix:**
1. Don't rely on `runtime.txt` — it's currently unreliable on Community Cloud.
2. When deploying, use the **Python version dropdown in "Advanced settings"**
   and pin it explicitly to **3.11 or 3.12**.
3. Pin exact package versions in `requirements.txt` (already done in this
   repo) instead of `>=` ranges, so pip can't silently resolve to an
   untested combination.
4. If you change the Python version after the app already exists, Community
   Cloud requires you to **delete and redeploy** the app — it can't be
   changed in place.
5. If it still segfaults, reboot the app from **Manage app → Reboot** to
   force a clean re-resolution of dependencies (stale cached environments
   are a secondary cause reported by other users).

### Favicon doesn't show / flickers

Streamlit's `page_icon` favicon support for SVG is inconsistent across
browsers. Use a PNG or ICO instead (this repo ships `assets/favicon.png`).

## Security design notes

The Quantum Lab challenges deliberately avoid `exec()` of user-submitted
Python. A public Streamlit deployment that runs arbitrary participant code is
a real risk (resource abuse, sandbox escape attempts). Instead, participants
compose circuits from a closed set of gate operations through the UI, and the
app runs the (trusted) simulation code. This keeps the challenge authentic —
real Qiskit, real state-vector math — without opening arbitrary code execution
to the public internet.

## Roadmap

Not implemented, to keep the initial migration shippable quickly:

- **Persistent progress** across sessions/devices (currently resets on
  browser refresh) — would need a lightweight store such as SQLite or a free
  Supabase/Firebase project.
- **Shot-based measurement** (counts/histogram) challenges using
  `qiskit-aer`, left out to keep the Community Cloud build fast and light.
- **Deep-linkable challenges** via `st.query_params` for direct sharing.

## License

MIT.
