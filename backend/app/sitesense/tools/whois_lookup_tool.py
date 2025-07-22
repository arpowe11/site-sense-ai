"""
DomainSearchTool: LangChain-compatible tool for performing WHOIS lookups on domain names.

This tool allows an agent to check the availability and registration details of a domain
using the `whois` Python library. It is wrapped in a LangChain `Tool` and can be
used by ReAct-style agents or integrated into custom agent chains.

Author: Alexander Powell
Version: v1.0
Dependencies:
    - whois

Usage:
    - Used to check domain registration details during domain validation or research tasks.
    - Returns a string field WHOIS record or an error message if the lookup fails.
"""


from langchain.tools import Tool
import whois


class DomainSearchTool(Tool):
    ...


domain_search_tool = DomainSearchTool()
