# YadaCoin HTTP surface used by this toolkit

Sources: `docs/API/*` and `yadacoin/http/node.py` on `pdxwebdev/yadacoin` (master, reviewed 2026-10-03).

## Node

- `GET /get-status`
- `GET /get-latest-block`
- `GET /get-block?hash=` or `?index=`
- `GET /get-height` and `/getheight`
- `GET /get-blocks`
- `GET /get-peers`
- `GET /get-mempool`
- `GET /get-pending-transaction`
- `GET /get-pending-transaction-ids`
- `GET /get-tested-nodes`
- `GET /network-topology`
- `GET /get-monitoring`
- `POST /newblock` (node peering; not wrapped)
- `POST /mine-block` (JWT)

## Explorer

- `GET /explorer-search?term=` optional `result_type`
  Matches height, public key, block/tx hash or id, rid, KEL hashes, identity username, file announcement fields, address, then mempool and failed equivalents.

## Wallet

- `GET /generate-wallet`
- `GET /wallet?address=`
- `GET /validate-address?address=`
- `GET /convert-public-key-to-address?public_key=`
- `GET /get-transaction-by-id?id=`
- `GET /get-transaction-confirmations?id=`
- `POST /unlock` body `key_or_wif` (key material)
- `POST /generate-child-wallet` JWT, body `index`
- `POST /send-transaction` JWT, body `address`, `value`, `from`

## Graph

All take `bulletin_secret`:

- `GET /get-graph-info`
- `GET /get-graph-friends`
- `GET /get-graph-friend-requests`
- `GET /get-graph-sent-friend-requests`
- `GET /get-graph-messages`
- `GET /get-graph-new-messages`
- `GET /get-graph-posts`

## Docs vs handlers

`docs/API/node` documents `POST /transaction`, `POST /create-raw-transaction`, and `POST /sign-raw-transaction`. The node handler list reviewed in `yadacoin/http/node.py` did not include those three routes in the `HANDLERS` excerpt. Confirm they are registered in another module before relying on them.
