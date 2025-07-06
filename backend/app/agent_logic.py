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
Date: 2025-07-05
"""

from dotenv import load_dotenv, find_dotenv
from typing import Any, Dict

from .sitesense.services.chat_memory import SiteSenseConversationMemory
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
        self.chat_memory: SiteSenseConversationMemory = SiteSenseConversationMemory()
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
        Engage with the AI agent by passing in a user query, retrieving context from memory,
        invoking the ReAct agent, caching the response, and updating the memory.

        Parameters:
            user_input (str): The user's question or prompt to pass to the AI agent.

        Returns:
            Dict[str, Any]: The full response from the agent, including any intermediate steps and output.
        """

        self._create_agent()
        memory_context = self.chat_memory.get_context()

        # Get the response from the ReAct Agent
        ai_response = self.agent_executor.invoke({
            "input": user_input,
            "memory_context": memory_context,
        })

        input_response = ai_response["input"]
        output_response = ai_response["output"]

        # Cache the ai_response
        cache_update_tool.run(info=(input_response, output_response))

        # Update the conversation memory
        self.chat_memory.append(user_input=input_response, ai_response=output_response)

        return ai_response
