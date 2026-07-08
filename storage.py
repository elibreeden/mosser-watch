import json
from pathlib import Path

SEEN_FILE = Path("seen_items.json")

def load_seen_item_ids(path: Path = SEEN_FILE) -> set[str]:
    if not path.exists():
        return set()

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()

    return set(data)

def save_seen_item_ids(item_ids: set[str], path: Path = SEEN_FILE) -> None:
    path.write_text(
        json.dumps(sorted(item_ids), indent=2),
        encoding="utf-8",
    )

def get_new_items(items: list[dict], seen_ids: set[str]) -> list[dict]:
    return [
        item for item in items
        if item.get("item_id") and item["item_id"] not in seen_ids
    ]
