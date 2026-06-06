# memory.py
# ARIA's memory system
# Short-term — current session, lives in RAM
# Long-term  — persists across sessions, lives on disk as JSON
#
# This solves production note point 3:
# "State needs to be persistent in case of crashes"

import json
import os
from datetime import datetime
from typing import Optional


MEMORY_FILE = "aria_memory.json"


class Memory:
    def __init__(self):
        self.short_term: dict = {}       # current session
        self.long_term: dict = {}        # persists to disk
        self._load_long_term()
        print(f"[Memory] Loaded {len(self.long_term)} past research sessions")

    # ─── Long-term — persists to disk ───────────────────────────

    def _load_long_term(self):
        """Load memory from disk on startup"""
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    self.long_term = json.load(f)
            except Exception as e:
                print(f"[Memory] Could not load memory file: {e}")
                self.long_term = {}
        else:
            self.long_term = {}

    def _save_long_term(self):
        """Persist memory to disk"""
        try:
            with open(MEMORY_FILE, "w") as f:
                json.dump(self.long_term, f, indent=2)
        except Exception as e:
            print(f"[Memory] Could not save memory: {e}")

    def remember(self, query: str, result: dict):
        """
        Store a completed research result in long-term memory.
        Key is the normalized query — lowercase, stripped.
        """
        key = self._normalize(query)

        self.long_term[key] = {
            "query": query,
            "result": result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "access_count": self.long_term.get(key, {}).get("access_count", 0) + 1,
        }

        self._save_long_term()
        print(f"[Memory] Stored research for: '{query}'")

    def recall(self, query: str) -> Optional[dict]:
        """
        Check if ARIA has researched this query before.
        Returns stored result if found, None if not.
        """
        key = self._normalize(query)

        if key in self.long_term:
            entry = self.long_term[key]
            print(f"[Memory] Found past research for: '{query}'")
            print(f"[Memory] Originally researched: {entry['timestamp']}")
            print(f"[Memory] Accessed {entry['access_count']} times before")
            return entry["result"]

        return None

    def forget(self, query: str):
        """Remove a specific research entry — force fresh research"""
        key = self._normalize(query)
        if key in self.long_term:
            del self.long_term[key]
            self._save_long_term()
            print(f"[Memory] Forgot research for: '{query}'")

    def list_memories(self) -> list:
        """Return all past research queries"""
        return [
            {
                "query": v["query"],
                "timestamp": v["timestamp"],
                "access_count": v["access_count"],
            }
            for v in self.long_term.values()
        ]

    # ─── Short-term — current session only ──────────────────────

    def set_context(self, key: str, value):
        """Store something in current session context"""
        self.short_term[key] = value

    def get_context(self, key: str):
        """Retrieve from current session context"""
        return self.short_term.get(key)

    def clear_context(self):
        """Clear session context — called between runs"""
        self.short_term = {}

    # ─── Helpers ────────────────────────────────────────────────

    def _normalize(self, query: str) -> str:
        """Normalize query for consistent key matching"""
        return query.lower().strip()
