import os

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from site_sense_lib.lib.whois_search import whois_lookup


class SiteSense:
    load_dotenv(find_dotenv(), override=True)

    def __init__(self, *, model: str = "", temp: float = 0.5, memory_data=None) -> None:
        self.llm = ChatOpenAI(model=model, temperature=temp)  # Initialize the LLM
        self.domains: list = [".com", ".org", ".edu", ".gov", ".mil", ".net", ".info", ".tech", ".design", ".app"]
        self.memory = ConversationBufferMemory(memory_key="history", return_messages=True)
        if memory_data:
            # Load memory data, converting from the serialized format
            self.memory.chat_memory.messages = self.deserialize_messages(memory_data)

    def generate_prompt(self) -> PromptTemplate:
        with open(os.environ["TEMPLATE_PATH"], 'r') as t:
            template = t.read()

        # Define a prompt template
        prompt_template = PromptTemplate(
            input_variables=["history", "input"],
            template=template
        )

        return prompt_template

    def chat_bot(self, user_input="") -> ConversationChain:
        # check for domain names manually, not with the AI for more accurate searches
        for domain in self.domains:
            if domain in user_input.lower():
                return whois_lookup(user_input)

        chatbot = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.generate_prompt(),
        )

        # Generate response
        response = chatbot({"input": user_input})
        parsed_text = self.parse_text(response["response"])

        return parsed_text

    def parse_text(self, text: str) -> str:
        return text.replace("AIMessage(content='", "").replace("')", "")

    def get_memory_data(self):
        """Returns the current state of the memory to be stored in the session in a serializable format"""
        return self.serialize_messages(self.memory.chat_memory.messages)

    def reset_memory_data(self):
        self.memory = ConversationBufferMemory(memory_key="history", return_messages=True)

    def serialize_messages(self, messages):
        """Converts HumanMessage, AIMessage objects into a serializable format"""
        serialized = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                serialized.append({"type": "human", "content": msg.content})
            elif isinstance(msg, AIMessage):
                serialized.append({"type": "ai", "content": msg.content})
        return serialized

    def deserialize_messages(self, serialized_messages):
        """Converts serialized messages back into HumanMessage and AIMessage objects"""
        deserialized = []
        for msg in serialized_messages:
            if msg["type"] == "human":
                deserialized.append(HumanMessage(content=msg["content"]))
            elif msg["type"] == "ai":
                deserialized.append(AIMessage(content=msg["content"]))
        return deserialized
