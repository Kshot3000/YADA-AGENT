"""Command line for the YadaCoin agent client."""

from __future__ import annotations

import argparse
import json
import sys

from yada_agent.client import YadaClient, YadaError


def _print(data: object) -> None:
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2))
    else:
        print(data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="yada", description="YadaCoin node agent CLI")
    parser.add_argument("--node", default=None, help="Node base URL (or set YADA_NODE)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status")
    sub.add_parser("height")
    sub.add_parser("latest")
    sub.add_parser("peers")
    sub.add_parser("mempool")
    sub.add_parser("topology")

    block = sub.add_parser("block")
    block.add_argument("--hash")
    block.add_argument("--index", type=int)

    search = sub.add_parser("search")
    search.add_argument("term")

    wallet = sub.add_parser("wallet")
    wallet.add_argument("address")

    valid = sub.add_parser("validate")
    valid.add_argument("address")

    tx = sub.add_parser("tx")
    tx.add_argument("id")

    args = parser.parse_args(argv)
    client = YadaClient(base_url=args.node)
    try:
        if args.cmd == "status":
            _print(client.status())
        elif args.cmd == "height":
            _print(client.height())
        elif args.cmd == "latest":
            _print(client.latest_block())
        elif args.cmd == "peers":
            _print(client.peers())
        elif args.cmd == "mempool":
            _print(client.mempool())
        elif args.cmd == "topology":
            _print(client.network_topology())
        elif args.cmd == "block":
            _print(client.block(hash=args.hash, index=args.index))
        elif args.cmd == "search":
            _print(client.search(args.term))
        elif args.cmd == "wallet":
            _print(client.wallet(args.address))
        elif args.cmd == "validate":
            _print(client.validate_address(args.address))
        elif args.cmd == "tx":
            _print(client.transaction(args.id))
        else:
            parser.error("unknown command")
    except YadaError as exc:
        print(f"error: {exc}", file=sys.stderr)
        if exc.body:
            print(exc.body, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
