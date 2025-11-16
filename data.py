# data.py
import json
import asyncio
from typing import Dict, Any
import time

class DataManager:
    """
    Thread-safe JSON data manager using asyncio.to_thread for file IO.
    """
    def __init__(self, filename: str):
        self.filename = filename
        self._lock = asyncio.Lock()
        self._data: Dict[str, Any] = {}
        # load synchronously at init time using to_thread
        try:
            asyncio.get_event_loop().run_until_complete(self._load())
        except RuntimeError:
            # event loop not running — fallback to plain load attempt
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except FileNotFoundError:
                self._data = {}

    async def _load(self):
        async with self._lock:
            def _read():
                try:
                    with open(self.filename, "r", encoding="utf-8") as f:
                        return json.load(f)
                except FileNotFoundError:
                    return {}
            self._data = await asyncio.to_thread(_read)

    async def save(self):
        async with self._lock:
            data_copy = dict(self._data)
            def _write():
                with open(self.filename, "w", encoding="utf-8") as f:
                    json.dump(data_copy, f, indent=2, ensure_ascii=False)
            await asyncio.to_thread(_write)

    def _ensure_user(self, user_id: str):
        if user_id not in self._data:
            self._data[user_id] = {
                "coins": 0,
                "inventory": {},
                "last_loot": 0,
                "last_daily": 0,
                "last_weekly": 0,
                "title": "Deck Swabber",
                "boosts": {},
                "total_loots": 0,
                "missions_completed": 0,
                "biggest_loot": 0
            }
        return self._data[user_id]

    # synchronous helper methods that mutate in-memory data.
    # call save() afterward to persist.
    def get_user(self, user_id: str):
        return self._ensure_user(user_id)

    def add_coins(self, user_id: str, amount: int):
        user = self._ensure_user(user_id)
        user["coins"] += amount
        user["total_loots"] = user.get("total_loots", 0)
        user["biggest_loot"] = max(user.get("biggest_loot", 0), amount)
        return user["coins"]

    def set_field(self, user_id: str, field: str, value):
        user = self._ensure_user(user_id)
        user[field] = value

    def add_item(self, user_id: str, item_name: str, amount: int = 1):
        user = self._ensure_user(user_id)
        inventory = user.setdefault("inventory", {})
        inventory[item_name] = inventory.get(item_name, 0) + amount

    def all_users(self):
        return dict(self._data)

    # convenience timestamp getters
    def get_timestamp(self, user_id: str, key: str):
        return self._ensure_user(user_id).get(key, 0)

    def set_timestamp(self, user_id: str, key: str, ts: float):
        self._ensure_user(user_id)[key] = ts
