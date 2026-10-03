# YADA-AGENT

Agent tools, a small website, and a Python client for the [YadaCoin](https://yadacoin.io/) blockchain.

Upstream node: [pdxwebdev/yadacoin](https://github.com/pdxwebdev/yadacoin)
Docs: [pdxwebdev.github.io/yadacoin](https://pdxwebdev.github.io/yadacoin/)

This repo is independent of the core node. It wraps the public HTTP API (node, explorer, wallet, graph) so agents and apps can talk to a YadaCoin node without embedding the full node.

## What is here

- `yada_agent/client.py` — async-free HTTP client for node, explorer, wallet, and graph endpoints
- `yada_agent/cli.py` — `yada` command line (`status`, `height`, `block`, `search`, `wallet`, `peers`)
- `web/index.html` — static explorer / node dashboard (no build step)
- `docs/API_SURFACE.md` — endpoint map taken from upstream docs and handlers
- `docs/BUGSCAN.md` — scan notes and how to re-run a local audit

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export YADA_NODE=http://127.0.0.1:8000
python -m yada_agent.cli status
python -m yada_agent.cli search 0
```

Open the dashboard:

```bash
python -m http.server 8080 --directory web
# then visit http://127.0.0.1:8080 and set the node URL
```

Default node URL is `http://127.0.0.1:8000` (upstream `serve_port`). Point it at any node you trust.

## Safety

- Do not send a private key, WIF, or seed to a remote node.
- `/unlock` and `/sign-raw-transaction` accept key material. This client refuses to call them unless `allow_key_material=True` and the host is loopback.
- JWT wallet routes (`/send-transaction`, `/generate-child-wallet`) need a bearer token from a local unlock.

## Protocol notes

YadaCoin is a proof-of-work L1 (Protocol v5 is a breaking upgrade). Addresses are Bitcoin-style P2PKH. Identity features include `did:yadacoin`, a KEL-style key event log, graph transactions, and a BSC wrapped asset (WYDA). This toolkit does not implement mining or consensus.
