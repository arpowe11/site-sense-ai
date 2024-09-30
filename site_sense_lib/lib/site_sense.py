import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


class SiteSense:
    # Load environment variables from .env file
    load_dotenv(find_dotenv(), override=True)

    def __init__(self, *, model: str = "", temp: float = 0.5, memory_data=None) -> None:
        self.llm: ChatOpenAI = ChatOpenAI(model=model, temperature=temp)
        self.chat_history: list = memory_data

    def get_prompt(self, usr_inp: str) -> str:
        """
        Opens the template and returns the prompt so the AI can
        generate the response based on the prompt.

        :param usr_inp: User input string
        :return: Formatted prompt string
        """
        with open(os.environ["TEMPLATE"], 'r') as text_file:
            template = text_file.read()

        # Combine chat memory into a single string
        memory_context = "\n".join(self.chat_history)

        # Update the template to include memory context
        prompt_template = PromptTemplate(
            input_variables=["memory_context", "user_input"],
            template=template
        )

        return prompt_template.format(memory_context=memory_context, user_input=usr_inp)

    # Function to get a response from the chatbot
    def get_response(self, user_input) -> str:
        prompt = self.get_prompt(user_input)
        response = self.llm.invoke(prompt)
        return response.content

    def update_memory(self, prompt, response) -> list:
        self.chat_history.append(f"Human: {prompt}")
        self.chat_history.append(f"Emily: {response}")

        if len(self.chat_history) > 10:
            self.chat_history.pop(0)

        return self.chat_history
