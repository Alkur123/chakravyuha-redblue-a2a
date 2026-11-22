"""Finch: read-only skill-market search for a matching remediation skill.

Uses only Finch's public search (no wallet, no account). Blue cites the top
matching skill next to each hardening rule. A failed search is logged, not
invented.
"""
from __future__ import annotations

from typing import Optional

import httpx

from formation import events

SEARCH = "https://www.finchtech.ai/api/market/search"


FALLBACKS = ("security threat model", "security")


class Finch:
    async def search(self, q: str) -> Optional[dict]:
        """Try the specific attack class first, then broader queries.
        Returns the top hit with the query that actually matched."""
        for query in (q, *FALLBACKS):
            try:
                async with httpx.AsyncClient(timeout=15) as c:
                    r = await c.get(SEARCH, params={"kind": "skill", "q": query})
                    body = r.json()
            except Exception as e:
                events.emit("sponsor", "finch", status="error", error=str(e)[:160])
                return None
            items = body.get("items", []) if isinstance(body, dict) else []
            events.emit("sponsor", "finch", status="search", q=query, results=len(items))
            if items:
                top = items[0]
                hit = {"name": top.get("name"), "slug": top.get("slug"),
                       "id": top.get("id"), "matched_query": query}
                events.emit("sponsor", "finch", status="cited", top=hit)
                return hit
        return None
