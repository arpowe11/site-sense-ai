import os

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


"""
When using this AI model, if you want to get response, do:
* response['response']  # get just the AI response
"""


class SiteSense:
    load_dotenv(find_dotenv(), override=True)

    def __init__(self, *, model: str = "", temp: int = 0) -> None:
        self.llm = ChatOpenAI(model=model, temperature=temp)  # Initialize the LLM
        self.memory = ConversationBufferMemory(memory_key="history", return_messages=True)

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
        chatbot = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.generate_prompt(),
        )

        response = chatbot({"input": user_input})
        return response

    def clear_history(self) -> None:
        self.memory = ConversationBufferMemory(memory_key="history", return_messages=True)
