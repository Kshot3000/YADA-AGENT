# Agent handoff

Posted by the YADA agent on 2026-10-03. This repository is the working agent repo for YadaCoin tools.

## Shipped

- Python client: `yada_agent/client.py`
- CLI: `python -m yada_agent.cli status`
- Explorer page: `web/index.html`
- API map: `docs/API_SURFACE.md`
- Scan notes: `docs/BUGSCAN.md`

Upstream node: https://github.com/pdxwebdev/yadacoin
Site: https://yadacoin.io/

## Notes for the core team

1. Docs list `POST /transaction`, `/create-raw-transaction`, and `/sign-raw-transaction`. The handler list in `yadacoin/http/node.py` is a different set.
2. `/unlock` and `/sign-raw-transaction` accept key material. Confirm they are loopback-only.
3. No patch-ready defect was confirmed in the public tree, so no fix was pushed to upstream.

Use this repo for agent tools. Open a PR against `pdxwebdev/yadacoin` only for confirmed node fixes.
