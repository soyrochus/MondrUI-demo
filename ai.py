#!/usr/bin/env python3
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from log_callback_handler import NiceGuiLogElementCallbackHandler
from dotenv import load_dotenv
import os
from typing import AsyncGenerator, Optional

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


class AIAgent:
    def __init__(self, model: str = 'gpt-4o-mini'):
        """Initialize the AI agent with memory capabilities."""
        # Set API key via environment variable
        if OPENAI_API_KEY:
            os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
            
        self.llm = ChatOpenAI(
            model=model, 
            streaming=True
        )
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )
        
    def get_conversation_history(self) -> list:
        """Get the current conversation history."""
        return self.memory.chat_memory.messages
    
    def clear_memory(self) -> None:
        """Clear the conversation memory."""
        self.memory.clear()
    
    async def send_message(
        self, 
        message: str, 
        callback_handler: Optional[NiceGuiLogElementCallbackHandler] = None
    ) -> AsyncGenerator[str, None]:
        """
        Send a message to the AI and get streaming response with memory.
        
        Args:
            message: The user's message
            callback_handler: Optional callback handler for logging
            
        Yields:
            str: Chunks of the AI response
        """
        # Get chat history for context
        chat_history = self.memory.chat_memory.messages
        
        # Prepare messages with history
        messages = chat_history + [HumanMessage(content=message)]
        
        # Configure callbacks
        config = None
        if callback_handler:
            config = RunnableConfig(callbacks=[callback_handler])
        
        # Stream the response
        response_content = ""
        async for chunk in self.llm.astream(messages, config=config):
            chunk_content = str(chunk.content) if chunk.content else ""
            response_content += chunk_content
            yield chunk_content
        
        # Save the conversation to memory
        self.memory.chat_memory.add_user_message(message)
        self.memory.chat_memory.add_ai_message(response_content)
    
    def get_conversation_count(self) -> int:
        """Get the number of message pairs in the conversation."""
        return len(self.memory.chat_memory.messages) // 2
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation for display purposes."""
        messages = self.memory.chat_memory.messages
        if not messages:
            return "New conversation"
        
        # Get the first user message as a summary
        for msg in messages:
            if isinstance(msg, HumanMessage):
                # Truncate long messages for display
                content = str(msg.content)
                if len(content) > 50:
                    content = content[:50] + "..."
                return content
        
        return "New conversation"
