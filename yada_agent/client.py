"""Thin client for a YadaCoin node HTTP API.

Endpoint names follow pdxwebdev/yadacoin docs and yadacoin/http handlers.
Key material is blocked unless the node is loopback and the caller opts in.
"""

from __future__ import annotations

import os
from typing import Any
from urllib.parse import urlparse

import requests


class YadaError(RuntimeError):
    def __init__(self, message: str, status: int | None = None, body: Any = None):
        super().__init__(message)
        self.status = status
        self.body = body


class YadaClient:
    def __init__(
        self,
        base_url: str | None = None,
        timeout: float = 20.0,
        token: str | None = None,
        allow_key_material: bool = False,
    ):
        self.base_url = (base_url or os.environ.get("YADA_NODE") or "http://127.0.0.1:8000").rstrip("/")
        self.timeout = timeout
        self.token = token
        self.allow_key_material = allow_key_material
        self.session = requests.Session()
        self.session.headers["Accept"] = "application/json"

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        url = f"{self.base_url}{path}"
        try:
            response = self.session.request(
                method,
                url,
                timeout=self.timeout,
                headers=self._headers(),
                **kwargs,
            )
        except requests.RequestException as exc:
            raise YadaError(f"{method} {url} failed: {exc}") from exc
        if response.status_code >= 400:
            raise YadaError(
                f"{method} {path} -> {response.status_code}",
                status=response.status_code,
                body=response.text[:2000],
            )
        if not response.content:
            return None
        ctype = response.headers.get("content-type", "")
        if "json" in ctype or response.text[:1] in "{[" :
            try:
                return response.json()
            except ValueError:
                return response.text
        return response.text

    def _require_local_keys(self) -> None:
        host = (urlparse(self.base_url).hostname or "").lower()
        if host not in {"127.0.0.1", "localhost", "::1"} or not self.allow_key_material:
            raise YadaError(
                "Refusing to send key material. Use a loopback node and allow_key_material=True."
            )

    # Node
    def status(self) -> Any:
        return self._request("GET", "/get-status")

    def latest_block(self) -> Any:
        return self._request("GET", "/get-latest-block")

    def height(self) -> Any:
        return self._request("GET", "/get-height")

    def block(self, hash: str | None = None, index: int | None = None) -> Any:
        params: dict[str, Any] = {}
        if hash:
            params["hash"] = hash
        if index is not None:
            params["index"] = index
        if not params:
            raise YadaError("block() needs hash or index")
        return self._request("GET", "/get-block", params=params)

    def peers(self) -> Any:
        return self._request("GET", "/get-peers")

    def mempool(self) -> Any:
        return self._request("GET", "/get-mempool")

    def tested_nodes(self) -> Any:
        return self._request("GET", "/get-tested-nodes")

    def network_topology(self) -> Any:
        return self._request("GET", "/network-topology")

    # Explorer
    def search(self, term: str, result_type: str | None = None) -> Any:
        params: dict[str, Any] = {"term": term}
        if result_type:
            params["result_type"] = result_type
        return self._request("GET", "/explorer-search", params=params)

    # Wallet (read)
    def wallet(self, address: str) -> Any:
        return self._request("GET", "/wallet", params={"address": address})

    def validate_address(self, address: str) -> Any:
        return self._request("GET", "/validate-address", params={"address": address})

    def public_key_to_address(self, public_key: str) -> Any:
        return self._request("GET", "/convert-public-key-to-address", params={"public_key": public_key})

    def transaction(self, tx_id: str) -> Any:
        return self._request("GET", "/get-transaction-by-id", params={"id": tx_id})

    def confirmations(self, tx_id: str) -> Any:
        return self._request("GET", "/get-transaction-confirmations", params={"id": tx_id})

    def generate_wallet(self) -> Any:
        """Asks the node to generate a seed. Only call this on a node you control."""
        return self._request("GET", "/generate-wallet")

    # Graph
    def graph_info(self, bulletin_secret: str) -> Any:
        return self._request("GET", "/get-graph-info", params={"bulletin_secret": bulletin_secret})

    def graph_friends(self, bulletin_secret: str) -> Any:
        return self._request("GET", "/get-graph-friends", params={"bulletin_secret": bulletin_secret})

    def graph_posts(self, bulletin_secret: str) -> Any:
        return self._request("GET", "/get-graph-posts", params={"bulletin_secret": bulletin_secret})

    def graph_messages(self, bulletin_secret: str) -> Any:
        return self._request("GET", "/get-graph-messages", params={"bulletin_secret": bulletin_secret})

    # Guarded write helpers
    def unlock(self, key_or_wif: str) -> Any:
        self._require_local_keys()
        data = self._request("POST", "/unlock", json={"key_or_wif": key_or_wif})
        if isinstance(data, dict):
            token = data.get("token") or data.get("jwt") or data.get("access_token")
            if token:
                self.token = token
        return data

    def send(self, address: str, value: str | float, from_address: str) -> Any:
        if not self.token:
            raise YadaError("send() needs a JWT. Unlock locally first.")
        return self._request(
            "POST",
            "/send-transaction",
            json={"address": address, "value": value, "from": from_address},
        )
