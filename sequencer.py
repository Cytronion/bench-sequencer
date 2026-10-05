"""Order a BCA lab session around shared apparatus.

An experiment starts only when every tool it needs is free.
Among ready experiments, prefer the one that releases the most
contested tool soonest.
"""

from __future__ import annotations

EXPERIMENTS = [
    {"id": "E1", "title": "Join plan on the college schema", "minutes": 40, "tools": ["sql-image"], "bench": "A"},
    {"id": "E2", "title": "Index vs full scan timing", "minutes": 30, "tools": ["sql-image"], "bench": "A"},
    {"id": "E3", "title": "Transaction rollback drill", "minutes": 35, "tools": ["sql-image"], "bench": "B"},
    {"id": "E4", "title": "Wireshark handshake capture", "minutes": 45, "tools": ["capture-laptop"], "bench": "C"},
    {"id": "E5", "title": "Subnet mask walkthrough", "minutes": 25, "tools": ["projector"], "bench": "Demo"},
    {"id": "E6", "title": "DNS trace and cache flush", "minutes": 30, "tools": ["capture-laptop"], "bench": "C"},
    {"id": "E7", "title": "ER diagram critique", "minutes": 20, "tools": ["projector"], "bench": "Demo"},
    {"id": "E8", "title": "Normalization to 3NF on paper", "minutes": 25, "tools": [], "bench": "Desk"},
]


def contest(experiments: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for exp in experiments:
        for tool in exp["tools"]:
            counts[tool] = counts.get(tool, 0) + 1
    return counts


def sequence(experiments: list[dict], session: int = 180) -> list[dict]:
    pending = [dict(e) for e in experiments]
    tool_free = {}
    clock_floor = 0
    card = []
    heat = contest(experiments)
    while pending:
        ready = []
        for exp in pending:
            start = max([tool_free.get(tool, 0) for tool in exp["tools"]] or [0])
            if start <= clock_floor or not exp["tools"]:
                ready.append((start, exp))
        if not ready:
            clock_floor = min(tool_free.get(t, 0) for e in pending for t in e["tools"])
            continue
        def rank(item):
            start, exp = item
            heat_score = sum(heat.get(t, 1) for t in exp["tools"]) or 1
            return (start, -heat_score, exp["minutes"])
        start, chosen = sorted(ready, key=rank)[0]
        if start + chosen["minutes"] > session:
            pending.remove(chosen)
            card.append({**chosen, "start": None, "note": "does not fit"})
            continue
        pending.remove(chosen)
        finish = start + chosen["minutes"]
        for tool in chosen["tools"]:
            tool_free[tool] = finish
        bottleneck = chosen["tools"][0] if chosen["tools"] else "none"
        card.append({**chosen, "start": start, "finish": finish, "bottleneck": bottleneck or "none"})
        clock_floor = min([e_start for e_start, _ in ready] or [finish])
    return card


if __name__ == "__main__":
    for row in sequence(EXPERIMENTS):
        if row["start"] is None:
            print(f"{row['id']}  skipped  {row['title']}")
        else:
            print(f"{row['start']:>3}–{row['finish']:<3}  {row['id']}  {row['title']}  via {row['bottleneck']}")
