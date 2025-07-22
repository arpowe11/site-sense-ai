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
    ...


cache_update_tool = CacheUpdateTool()

