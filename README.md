# Defending AI Agents Against Prompt Injection

A small research project testing whether a simple AI agent is vulnerable to prompt injection attacks, and whether a known, lightweight defense (system/user role separation + explicit untrusted-content tagging) actually works.

Built after reading about the July 2026 incident in which AI agents from OpenAI's internal security testing bypassed their isolation and breached Hugging Face's infrastructure through a chain of real vulnerabilities and exposed credentials, a case that highlighted how AI agents given real capabilities can be manipulated or misdirected in ways simple prompting doesn't protect against.

**Full write-up: [REPORT.md](REPORT.md)**

## What I found

| | Phase 1: Naive Agent | Phase 2: Hardened Agent |
|---|---|---|
| Attack Success Rate | **42.9%** (3/7) | **0.0%** (0/7) |

![Attack success rate comparison](comparison_chart.png)

A simple agent that pastes document content directly into its prompt fell for 3 of 7 tested injection techniques, including direct instruction overrides, fake system messages, and instructions hidden in HTML comments. After adding structural defenses, role separation and explicit `<untrusted_data>` tagging, the same 7 attacks all failed.

## How it works

**Phase 1 — `toy_agent.py`:** A minimal summarization agent, built the way most basic tutorials show it: document text pasted directly into one prompt, no protection.

**Phase 2 — `toy_agent_v2.py`:** A hardened version with tool-calling access (a mock `read_document` and a high-risk mock `send_email` tool), defended with:
- A system-level instruction establishing that untrusted content is data, never commands
- Document content wrapped in `<untrusted_data>` XML tags for a clear structural boundary

Both agents were tested against the same 7 injection techniques (direct override, fake system message, roleplay trick, HTML-comment injection, fake authority claim, multilingual injection, reward bribe), plus one normal control case.

No real system was attacked or probed. All "attacks" were run against a small, self-contained toy agent built for this project, using mock tools and simulated documents.

## Running it yourself

**Requirements:** Python 3.8+, a free Groq API key (console.groq.com, no credit card needed)

```bash
pip install groq python-dotenv matplotlib
```

Create a `.env` file in this folder:
```
GROQ_API_KEY=your-key-here
```

**Run the baseline test:**
```bash
python test_injections.py
```
Saves results to `injection_results.csv`.

**Run the hardened test:**
```bash
python test_injections_v2.py
```
Saves results to `injection_v2_results.csv`.

**Generate the comparison chart:**
```bash
python make_comparison_chart.py
```
Reads both CSVs directly (no manual number entry) and saves `comparison_chart.png`.

## Files in this repo

| File | Purpose |
|---|---|
| `toy_agent.py` | Phase 1: naive, vulnerable agent |
| `toy_agent_v2.py` | Phase 2: hardened agent with defenses |
| `test_injections.py` | Test harness for Phase 1 |
| `test_injections_v2.py` | Test harness for Phase 2 |
| `injection_results.csv` | Raw Phase 1 results |
| `injection_v2_results.csv` | Raw Phase 2 results |
| `make_comparison_chart.py` | Generates the comparison chart from the CSVs |
| `comparison_chart.png` | Summary chart |
| `REPORT.md` | Full write-up: motivation, method, findings, defense techniques (old vs. new), discussion, limitations |

## Why I built this

I'm a B.Tech CS graduate exploring security and AI research. This project was a way to test a real, documented vulnerability class on a system I built myself, measure it honestly, then fix it and measure again, rather than just reading about the problem.
