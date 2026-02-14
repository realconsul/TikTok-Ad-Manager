"""Simple Supabase REST client for storing and reading analytics artifacts."""
from __future__ import annotations

from typing import Any

import requests


class SupabaseClient:
    def __init__(self, url: str, key: str) -> None:
        self.base_url = url.rstrip("/")
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }

    def insert_rows(self, table: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        response = requests.post(
            f"{self.base_url}/rest/v1/{table}", headers=self.headers, json=rows, timeout=30
        )
        response.raise_for_status()
        return response.json()

    def upsert_rows(
        self,
        table: str,
        rows: list[dict[str, Any]],
        on_conflict: str,
    ) -> list[dict[str, Any]]:
        headers = self.headers | {"Prefer": "resolution=merge-duplicates,return=representation"}
        response = requests.post(
            f"{self.base_url}/rest/v1/{table}?on_conflict={on_conflict}",
            headers=headers,
            json=rows,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def select(
        self,
        table: str,
        select_expr: str = "*",
        limit: int | None = None,
        order: str | None = None,
        filters: dict[str, str] | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, str | int] = {"select": select_expr}
        if limit:
            params["limit"] = limit
        if order:
            params["order"] = order
        if filters:
            params.update(filters)
        response = requests.get(
            f"{self.base_url}/rest/v1/{table}",
            headers=self.headers,
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
