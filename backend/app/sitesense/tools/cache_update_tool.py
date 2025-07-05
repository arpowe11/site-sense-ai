"""
CacheUpdateTool: LangChain-compatible tool for storing LLM responses in a persistent cache.

This tool is intended to be used outside the agent loop after a final answer has been generated.
It receives a serialized input containing the original prompt and the agent's response, and
stores this key-value pair in a caching backend (e.g., PostgresSQL via SiteSenseCache).

Author: Alexander Powell
Version: 1.0
Dependencies:
    - SiteSenseCache (custom PostgresSQL-based cache class)

Usage:
    - Call this tool manually or as part of a post-processing step.
    - Expects a tuple with the prompt and the llm_response

Notes:
    - This tool does not retrieve data. For lookups, use CacheLookupTool.
    - Useful for persisting responses to improve agent efficiency and reduce cost.
"""


from langchain.tools import Tool
from ..services.chat_cache import SiteSenseCache

import os


class CacheUpdateTool(Tool):
    def __init__(self):
        super().__init__(
            name="Cache Update Tool",
            description="Invokes the update function for the cacheing service",
            func=self.run
        )

    def run(self, info: tuple, *args, **kwargs) -> str:
        prompt = info[0]
        llm_response = info[1]
        cache = SiteSenseCache(os.getenv("TEST_DB_CACHE"))

        try:
            print("[+] Updating the cache with {prompt} and {ai_response}".format(prompt=prompt, ai_response=llm_response))
            cache.update(prompt=prompt, llm_response=llm_response)
        except Exception as e:
            return f"A problem occurred while updating the cache: {e}"


cache_update_tool = CacheUpdateTool()

