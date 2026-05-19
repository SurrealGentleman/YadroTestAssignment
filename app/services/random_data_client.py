from typing import Any

import httpx


class RandomDataToolsClient:
    def __init__(self, base_url: str, timeout: float = 20.0) -> None:
        self.base_url = base_url
        self.timeout = timeout

    def fetch_people(self, count: int) -> list[dict[str, Any]]:
        response = httpx.get(
            self.base_url,
            params={"count": count},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()

        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
        if isinstance(payload, dict):
            return [payload]
        return []

