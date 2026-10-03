# Bug scan notes — 2026-10-03

Scope: public tree and docs of `pdxwebdev/yadacoin`, plus `https://yadacoin.io/`. This was not a full audit of the node, bridge contracts, password-manager clients, or the marketing site source (the site source is not in the node repo).

No confirmed, patch-ready defect was isolated in this pass, so no fix was pushed to upstream. Findings below are review notes for the core team.

## Findings

1. Key material on HTTP. Docs describe `POST /sign-raw-transaction` with `private_key` and `POST /unlock` with `key_or_wif`. If these routes are reachable beyond localhost, a node operator or network observer can steal funds. Recommend binding them to loopback, requiring JWT plus a local-only flag, or removing server-side signing entirely.
2. Route docs drift. `docs/API/node/index.md` lists `/transaction`, `/create-raw-transaction`, and `/sign-raw-transaction`. The handler table in `yadacoin/http/node.py` exposes a different set (`/newblock`, `/get-mempool`, `/mine-block`, `/network-topology`, and others). Agents built only from the docs will call missing routes. The client in this repo follows the handler list for reads and documents the mismatch.
3. `yadacoin.io` fetch did not expose a public explorer or node endpoint. The static dashboard here therefore defaults to `127.0.0.1:8000`. A documented public read-only endpoint would make the explorer usable without running a node.
4. GitHub code search for `TODO` / `FIXME` / `XXX` in the Python tree returned no hits. That does not mean the tree is clean; it only means those markers are not used.

## Not scanned

- Solidity bridge (`Bridge.sol`, `KeyLogRegistry.sol`) — a Feb 2026 Zealynx audit exists; re-check fixes against that report separately.
- Password manager clients under `clients/password-manager`.
- Protocol v5 migration scripts.
- Runtime tests. They need MongoDB and a node (`pytest` in the upstream repo).

## How to continue

```bash
git clone https://github.com/pdxwebdev/yadacoin.git
cd yadacoin
python -m pip install -r requirements.txt pytest
pytest tests/unittests -q
```

Fixes for upstream should be a fork + PR to `pdxwebdev/yadacoin`, not silent commits. Agent-side tools belong in this repo.
