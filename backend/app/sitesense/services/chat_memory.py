"""
Memory modules for SiteSense AI Agent.

This module provides two memory implementations used to maintain conversation history
for a ReAct-style agent:

1. SiteSenseAIMemory:
    - A simple list-based memory that stores a rolling window of the last 10 messages.
    - Appends raw chat message strings.
    - Removes the oldest message when the limit is exceeded.

2. SiteSenseConversationMemory:
    - A deque-based memory implementation optimized for structured dialogue storage.
    - Stores user-AI message pairs in a consistent format.
    - Supports fixed-length history via maxlen parameter.

These memory classes are used to build a memory context string that gets passed to the
agent prompt, enabling contextual reasoning across turns.

Author: Alexander Powell
Version: v1.0
"""


from collections import deque


class SiteSenseAIMemory:
    def __init__(self):
        self.chat_history: list = []

    def append(self, chat_messages: str):
        if len(self.chat_history) > 10:
            self.remove()

        self.chat_history.append(chat_messages)

    def remove(self):
        self.chat_history.pop(0)

    def get_chat_history(self):
        return "".join(self.chat_history)


class SiteSenseConversationMemory:
    def __init__(self, maxlen=10):
        self.history = deque(maxlen=maxlen)

    def append(self, user_input, ai_response):
        self.history.append(f"Human: {user_input}\nAI: {ai_response}")

    def get_context(self):
        return "\n".join(self.history)
    