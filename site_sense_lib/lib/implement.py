"""
Here is some code that can possibly be implemented in version 1.2 of SiteSenseAI

Do not use the entire test llm, only the parts that works with the memory to try and better improve the
AIs engagment with the conversation

Possibly might have to do a whole re-write for version 1.2 of the AI just to make the flow
of the AI work better, try to not have to do that lol
"""


#############################################################
#  Test code for a new way to implement memory into the AI  #
#############################################################

from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.llms.openai import OpenAI  # We use ChatOpenAI


def generate_prompt(user_input, memory_buffer):
    # Retrieve context from memory buffer
    context = memory_buffer.get_context()

    # Format the prompt using the context and user input
    return prompt_template.format(context=context, user_input=user_input)


def process_input(user_input, llm, memory_buffer):
    # Generate the prompt
    prompt = generate_prompt(user_input, memory_buffer)
    
    # Get the response from the LLM
    response = llm(prompt)
    
    # Update memory buffer with the new interaction
    memory_buffer.update(user_input, response)
    
    return response


# Define the prompt template with placeholders for context and user input
prompt_template = PromptTemplate(
    input_variables=["context", "user_input"],
    template="""
    {context}

    User: {user_input}
    Assistant:
    """
)

# Initialize memory buffer
memory_buffer = ConversationBufferMemory()

# Initialize the language model
llm = OpenAI(model="gpt-4")


# Example conversation
user_input1 = "What's the weather today?"
response1 = process_input(user_input1, llm, memory_buffer)
print("Response 1:\n", response1)

user_input2 = "Do I need an umbrella?"
response2 = process_input(user_input2, llm, memory_buffer)
print("Response 2:\n", response2)
