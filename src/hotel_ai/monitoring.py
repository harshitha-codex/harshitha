from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class RecommendationMonitor:
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def record(self, event: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        entry = {
            "event": event,
            "payload": payload or {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.events.append(entry)
        return entry

    def summary(self) -> dict[str, Any]:
        counts: dict[str, int] = {}
        for entry in self.events:
            name = str(entry["event"])
            counts[name] = counts.get(name, 0) + 1
        return {
            "total_events": len(self.events),
            "event_counts": counts,
            "last_event": self.events[-1] if self.events else None,
        }
