import os
from dotenv import load_dotenv, find_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory


class SiteSense:
    load_dotenv(find_dotenv(), override=True)
    
    def __init__(self, *, model: str = "", temp: int = 0) -> None:
        self.llm = ChatOpenAI(model=model, temperature=temp)  # Initialize the LLM
        self.message_history = ChatMessageHistory()  # Initialize message history
    
    def create_response(self, question: str) -> str:
        with open(os.environ["TEMPLATE_PATH"], 'r') as t:
            template = t.read()

        history = "\n".join([msg.content for msg in self.message_history.messages])
        prompt_template = PromptTemplate.from_template(template=template)
        prompt = prompt_template.format(history=history, q=question)

        self.message_history.add_user_message(question)
        return prompt
    
    def stream_response(self, prompt: str = "") -> str:
        # Stream the output and accumulate it into a single message
        ai_message = ""
        for chunk in self.llm.stream(prompt):
            print(chunk.content, end="")
            ai_message += chunk.content  # Accumulate all chunks for the ai history
        
        self.message_history.add_ai_message(ai_message)
        print("\n")

        return ai_message
    
    def clear_history(self):
        self.message_history = ChatMessageHistory()

