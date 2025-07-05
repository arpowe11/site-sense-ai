"""
CacheTool: LangChain-compatible tool for performing cache lookups on previous user questions.

This tool allows an agent to check if a cached response exists for a given user input before
generating a new response. It is designed to be used in ReAct-style agents as a first step
in the reasoning chain to avoid redundant computation.

Author: Alexander Powell
Version: 1.0
Dependencies:
    - A custom cache implementation (e.g., SiteSenseCache using PostgreSQL)

Usage:
    - The agent calls this tool with a question as input.
    - The tool performs a lookup in a persistent cache (to be implemented in `_run`).
    - If a cached response is found, it should be returned.
    - Otherwise, a cache miss message or empty string can be returned.

Note:
    - This tool is for lookup only. Cache updates are be handled separately.
"""


from langchain.tools import Tool
from ..services.chat_cache import SiteSenseCache

import os


class CacheLookupTool(Tool):
    def __init__(self):
        super().__init__(
            name="Cache Lookup Tool",
            description="Cache tool that you will use to cache human inputs and ai responses",
            func=self._run
        )

    def _run(self, prompt: str, *args, **kwargs) -> str | None:
        cache = SiteSenseCache(os.getenv("TEST_DB_CACHE"))
        try:
            print("[+] Doing lookup for {question}".format(question=prompt))
            return cache.lookup(prompt=prompt) or None
        except Exception as e:
            return f"A problem occurred: {e}"


cache_lookup_tool = CacheLookupTool()
