"""
agent_logic.py

AI logic for the WordPress plugin.
This is the entry point that gets all the services and tools for the AI.

Dependencies:
    - langchain
    - python-dotenv
    - whois_lookup

Author: Alexander Powell
Version: v1.4
Date: 2025-06-16
"""

from dotenv import load_dotenv, find_dotenv
from typing import Any, Dict

from .sitesense.services.chat_memory import SiteSenseAIMemory
from .sitesense.tools import *

from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate


class SiteSenseAI:
    def __init__(self, model=None, temp=0.5, *, config=None):
        load_dotenv(find_dotenv(), override=True)

        if config is None:
            raise ValueError("Config file must be provided")

        if model is None:
            model: str = config["AI_MODEL"]

        self.agent_emily: ChatOpenAI = ChatOpenAI(model=model, temperature=temp)  # NOQA
        self.chat_memory: SiteSenseAIMemory = SiteSenseAIMemory()
        self.agent_executor: AgentExecutor
        self.prompt_template: Any = config["TEMPLATES_DIR"]

    def _get_prompt_template(self) -> PromptTemplate:  # NOQA
        with open(self.prompt_template) as template_file:
            template = template_file.read()
            template_file.close()

        prompt = PromptTemplate(
            input_variables=['agent_scratchpad', 'input', 'tool_names', 'tools', 'memory_context'],
            template=template
        )

        return prompt


    def _get_memory(self) -> SiteSenseAIMemory:
        return self.chat_memory

    def _update_memory(self, context: str):
        self.chat_memory.append(context)

    def _create_agent(self):
        prompt = self._get_prompt_template()
        tools: list = [cache_lookup_tool, domain_search_tool]

        agent = create_react_agent(self.agent_emily, tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )


    def engage(self, user_input: str) -> Dict[str, Any]:
        """
        Entry point to engage with the AI Agent and ask it questions.

        :param user_input:
        :return ai_response:
        """

        self._create_agent()

        # FIXME: Memory does not work, needs debugging and to be fixed or reimplemented
        memory_context = self.chat_memory.get_chat_history()

        # Get the response from the ReAct Agent
        ai_response = self.agent_executor.invoke({
            "input": user_input,
            "memory_context": memory_context,
        })

        # Cache the ai_response
        cache_update_tool.run(info=(ai_response["input"], ai_response["output"]))

        # Create the context for the memory and update the chat memory
        context: str = f"Human: {user_input}\nAI: {ai_response}"
        # print("[+] Input:", ai_response["input"])
        # print("[+] Output:", ai_response["output"])

        self.chat_memory.append(context)

        return ai_response
