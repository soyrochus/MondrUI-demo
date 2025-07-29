#!/usr/bin/env python3
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from log_callback_handler import NiceGuiLogElementCallbackHandler
from dotenv import load_dotenv
import os
from typing import AsyncGenerator, Optional, List

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


class AIAgent:
    """
    Modern AI Agent with conversation memory using LangChain 0.3+ best practices.
    
    This implementation follows the current LangChain recommendations:
    - Uses direct message storage instead of deprecated ConversationBufferMemory
    - Implements message trimming to manage memory usage
    - Compatible with LangGraph persistence patterns
    - No deprecation warnings
    """
    def __init__(self, model: str = 'gpt-4o-mini', max_messages: int = 100):
        """Initialize the AI agent with memory capabilities."""
        # Set API key via environment variable
        if OPENAI_API_KEY:
            os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
            
        self.llm = ChatOpenAI(
            model=model, 
            streaming=True
        )
        # Modern approach: store messages directly instead of using deprecated memory classes
        self.chat_history: List[BaseMessage] = []
        self.max_messages = max_messages
        
        # System message to help AI understand MondrUI capabilities
        self.system_message = SystemMessage(content="""
You are an AI assistant with the ability to create interactive forms using MondrUI. 

When users request structured information or need to submit data (like bug reports, feedback, help requests, surveys, etc.), you can generate MondrUI JSON specifications to create interactive forms.

To create a form, include a JSON code block in your response with this format:
```json
{
  "type": "ui.render",
  "component": "Form",
  "props": {
    "title": "Form Title",
    "fields": [
      {"id": "field1", "label": "Field Label", "type": "text", "required": true},
      {"id": "field2", "label": "Description", "type": "textarea", "required": false},
      {"id": "field3", "label": "Priority", "type": "radio", "options": {"low": "Low", "high": "High"}, "value": "low"},
      {"id": "field4", "label": "Features", "type": "checkboxGroup", "options": {"feature1": "Feature 1", "feature2": "Feature 2"}, "value": ["feature1"]},
      {"id": "field5", "label": "Rating", "type": "slider", "min": 1, "max": 10, "minLabel": "Poor", "maxLabel": "Excellent", "value": 5}
    ],
    "actions": [
      {"label": "Submit", "action": "submit_form"}
    ]
  }
}
```

Available components:
- Form: Generic form component with full field type support
- Container: Layout container (vertical, horizontal, grid)
- Text: Text display (labels, headings)
- Input: Basic input fields (text, textarea, select, checkbox, number)
- Button: Action buttons
- Radio: Radio button groups for exclusive selection
- CheckboxGroup: Multiple checkbox selection
- Slider: Range sliders with optional semantic labels

Available field types for forms:
- "text": Text input
- "textarea": Multi-line text input  
- "select": Dropdown selection
- "checkbox": Single checkbox
- "number": Numeric input
- "radio": Radio button group (exclusive selection) - requires "options" object
- "checkboxGroup": Multiple checkboxes (inclusive selection) - requires "options" object
- "slider": Range slider - supports "min", "max", "step", "minLabel", "maxLabel", "showValue"

Radio button options format: {"value1": "Label 1", "value2": "Label 2"}
CheckboxGroup options format: {"value1": "Label 1", "value2": "Label 2"}  
CheckboxGroup value format: ["value1", "value2"] (array of selected values)

Slider properties:
- min/max: numeric range
- step: increment value  
- value: current/default value
- minLabel/maxLabel: semantic labels for endpoints (e.g., "Unhappy"/"Happy")
- showValue: boolean to display current value
- labelAlways: boolean to always show slider labels

Available actions: submit_bug, submit_help, submit_feedback, submit_form

Use forms when users:
- Want to report bugs or issues
- Need to provide structured feedback  
- Request help or support
- Need surveys or preference collection
- Want to select from options (radio for exclusive, checkboxGroup for multiple)
- Need to rate or scale something (slider)
- Need to submit any structured data

Always explain what the form is for before presenting it.
""")
        
    def get_conversation_history(self) -> List[BaseMessage]:
        """Get the current conversation history."""
        return self.chat_history.copy()
    
    def clear_memory(self) -> None:
        """Clear the conversation memory."""
        self.chat_history.clear()
    
    def _trim_messages_if_needed(self) -> None:
        """Trim messages to keep within max_messages limit."""
        if len(self.chat_history) > self.max_messages:
            # Keep the most recent messages, ensuring we maintain pairs
            excess = len(self.chat_history) - self.max_messages
            # Remove from the beginning, but try to keep message pairs intact
            if excess % 2 == 1:
                excess += 1  # Remove one more to keep pairs
            self.chat_history = self.chat_history[excess:]
    
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
        # Add user message to history
        user_message = HumanMessage(content=message)
        
        # Prepare messages with system message and history (include current message)
        messages = [self.system_message] + self.chat_history + [user_message]
        
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
        self.chat_history.append(user_message)
        self.chat_history.append(AIMessage(content=response_content))
        
        # Trim messages if we've exceeded the limit
        self._trim_messages_if_needed()
    
    def get_conversation_count(self) -> int:
        """Get the number of message pairs in the conversation."""
        return len(self.chat_history) // 2
    
    def get_memory_stats(self) -> dict:
        """Get detailed memory statistics."""
        human_messages = sum(1 for msg in self.chat_history if isinstance(msg, HumanMessage))
        ai_messages = sum(1 for msg in self.chat_history if isinstance(msg, AIMessage))
        
        return {
            "total_messages": len(self.chat_history),
            "human_messages": human_messages,
            "ai_messages": ai_messages,
            "conversation_turns": min(human_messages, ai_messages),
            "max_messages": self.max_messages,
            "memory_usage_percent": (len(self.chat_history) / self.max_messages) * 100
        }
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation for display purposes."""
        if not self.chat_history:
            return "New conversation"
        
        # Get the first user message as a summary
        for msg in self.chat_history:
            if isinstance(msg, HumanMessage):
                # Truncate long messages for display
                content = str(msg.content)
                if len(content) > 50:
                    content = content[:50] + "..."
                return content
        
        return "New conversation"
