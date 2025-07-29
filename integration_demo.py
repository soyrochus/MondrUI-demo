#!/usr/bin/env python3
"""
Integration demo showing MondrUI with AI chat functionality.
This demonstrates the complete integration of AI chat with dynamic UI generation.
"""

import asyncio
from nicegui import ui, app
from ai import AIAgent
from mondrui import render_ui, register_component, create_component, BaseComponent


class IntegratedChatApp:
    """Integrated chat application with AI and MondrUI."""
    
    def __init__(self):
        self.ai_agent = AIAgent()
        self.setup_custom_components()
        self.setup_ui()
    
    def setup_custom_components(self):
        """Set up custom components for the integrated demo."""
        
        def memory_stats_render(props, renderer):
            """Render memory statistics component."""
            stats = props.get('stats', {})
            
            with ui.card().classes('p-4 bg-blue-50'):
                ui.label('Memory Statistics').classes('font-bold text-lg mb-2')
                with ui.column().classes('gap-2'):
                    ui.label(f"Total Messages: {stats.get('total_messages', 0)}")
                    ui.label(f"Memory Size: {stats.get('memory_size', 0)} characters")
                    ui.label(f"Last Update: {stats.get('last_update', 'Never')}")
        
        def chat_message_render(props, renderer):
            """Render a chat message component."""
            role = props.get('role', 'user')
            content = props.get('content', '')
            timestamp = props.get('timestamp', '')
            
            bg_class = 'bg-blue-100' if role == 'user' else 'bg-gray-100'
            
            with ui.card().classes(f'p-3 mb-2 {bg_class}'):
                with ui.row().classes('w-full justify-between items-start'):
                    with ui.column().classes('flex-1'):
                        ui.label(f"{role.title()}:").classes('font-bold text-sm')
                        ui.label(content).classes('text-sm')
                    if timestamp:
                        ui.label(timestamp).classes('text-xs text-gray-500')
        
        # Register custom components
        MemoryStatsComponent = create_component(memory_stats_render)
        ChatMessageComponent = create_component(chat_message_render)
        
        register_component('MemoryStats', MemoryStatsComponent)
        register_component('ChatMessage', ChatMessageComponent)
    
    def setup_ui(self):
        """Set up the main UI."""
        ui.query('.nicegui-content').classes('p-0')
        
        with ui.column().classes('h-screen w-full'):
            # Header
            self.render_header()
            
            # Main content area
            with ui.row().classes('flex-1 w-full'):
                # Sidebar with memory stats
                self.render_sidebar()
                
                # Chat area
                self.render_chat_area()
    
    def render_header(self):
        """Render the application header using MondrUI."""
        header_spec = {
            "type": "ui.render",
            "component": "Container",
            "props": {
                "layout": "horizontal",
                "style": {"classes": ["w-full", "p-4", "bg-blue-600", "text-white"]},
                "children": [
                    {
                        "component": "Text",
                        "props": {
                            "text": "MondrUI + AI Integration Demo",
                            "variant": "h1",
                            "style": {"classes": ["text-white", "flex-1"]}
                        }
                    },
                    {
                        "component": "Button",
                        "props": {
                            "label": "Clear Chat",
                            "variant": "secondary",
                            "action": "clear_chat"
                        }
                    }
                ]
            }
        }
        
        try:
            render_ui(header_spec)
        except Exception as e:
            ui.label(f"Header render error: {e}").classes('text-red-500')
    
    def render_sidebar(self):
        """Render the sidebar with memory statistics."""
        with ui.column().classes('w-80 bg-gray-50 p-4 h-full'):
            ui.label('AI Memory Status').classes('text-lg font-bold mb-4')
            
            # Memory stats using custom component
            stats = self.ai_agent.get_memory_stats()
            memory_stats_spec = {
                "type": "ui.render",
                "component": "MemoryStats",
                "props": {
                    "stats": stats
                }
            }
            
            try:
                render_ui(memory_stats_spec)
            except Exception as e:
                ui.label(f"Memory stats error: {e}").classes('text-red-500')
            
            ui.separator().classes('my-4')
            
            # Action buttons
            with ui.column().classes('gap-2'):
                ui.button('Export Memory', on_click=self.export_memory).classes('w-full')
                ui.button('Import Memory', on_click=self.import_memory).classes('w-full')
                ui.button('Reset Memory', on_click=self.reset_memory).classes('w-full')
    
    def render_chat_area(self):
        """Render the main chat area."""
        with ui.column().classes('flex-1 h-full p-4'):
            # Chat history container
            self.chat_container = ui.column().classes('flex-1 overflow-auto border rounded p-4 mb-4')
            
            # Load existing messages
            self.refresh_chat_history()
            
            # Input area
            with ui.row().classes('w-full gap-2'):
                self.message_input = ui.input(
                    placeholder='Type your message here...',
                    on_change=self.on_input_change
                ).classes('flex-1')
                
                ui.button('Send', on_click=self.send_message).classes('px-6')
                
                # Quick actions using MondrUI
                quick_actions_spec = {
                    "type": "ui.render",
                    "component": "Container",
                    "props": {
                        "layout": "horizontal",
                        "style": {"classes": ["gap-2"]},
                        "children": [
                            {
                                "component": "Button",
                                "props": {
                                    "label": "Bug Report",
                                    "variant": "secondary",
                                    "action": "show_bug_form"
                                }
                            },
                            {
                                "component": "Button",
                                "props": {
                                    "label": "Help",
                                    "variant": "secondary", 
                                    "action": "show_help"
                                }
                            }
                        ]
                    }
                }
                
                try:
                    render_ui(quick_actions_spec)
                except Exception as e:
                    ui.label(f"Quick actions error: {e}").classes('text-red-500 text-xs')
    
    def refresh_chat_history(self):
        """Refresh the chat history display."""
        self.chat_container.clear()
        
        messages = self.ai_agent.get_conversation_history()
        for msg in messages:
            role = 'user' if isinstance(msg, type(msg)) and hasattr(msg, 'content') else 'assistant'
            # Simple role detection - in a real app you'd import the message types
            if 'Human' in str(type(msg)):
                role = 'user'
            elif 'AI' in str(type(msg)):
                role = 'assistant'
                
            message_spec = {
                "type": "ui.render",
                "component": "ChatMessage",
                "props": {
                    "role": role,
                    "content": str(msg.content),
                    "timestamp": ""
                }
            }
            
            try:
                with self.chat_container:
                    render_ui(message_spec)
            except Exception as e:
                with self.chat_container:
                    ui.label(f"Message render error: {e}").classes('text-red-500 text-xs')
    
    def on_input_change(self, e):
        """Handle input changes for real-time features."""
        # Could add typing indicators or other real-time features here
        pass
    
    async def send_message(self):
        """Send a message and get AI response."""
        if not self.message_input.value.strip():
            return
        
        user_message = self.message_input.value.strip()
        self.message_input.value = ''
        
        # Add user message to chat
        with self.chat_container:
            user_spec = {
                "type": "ui.render",
                "component": "ChatMessage",
                "props": {
                    "role": "user",
                    "content": user_message
                }
            }
            render_ui(user_spec)
        
        # Show typing indicator
        with self.chat_container:
            typing_indicator = ui.label("AI is typing...").classes('text-gray-500 italic')
        
        try:
            # Get AI response using the streaming method
            response_content = ""
            async for chunk in self.ai_agent.send_message(user_message):
                response_content += chunk
            
            # Remove typing indicator
            typing_indicator.delete()
            
            # Add AI response to chat
            with self.chat_container:
                ai_spec = {
                    "type": "ui.render",
                    "component": "ChatMessage", 
                    "props": {
                        "role": "assistant",
                        "content": response_content
                    }
                }
                render_ui(ai_spec)
            
            # Scroll to bottom
            ui.run_javascript('document.querySelector(".chat-container").scrollTop = document.querySelector(".chat-container").scrollHeight')
            
        except Exception as e:
            typing_indicator.delete()
            with self.chat_container:
                ui.label(f"Error getting AI response: {e}").classes('text-red-500')
    
    def export_memory(self):
        """Export chat memory."""
        try:
            memory_data = self.ai_agent.get_conversation_history()
            ui.notify(f"Memory exported: {len(memory_data)} messages", type='positive')
        except Exception as e:
            ui.notify(f"Export failed: {e}", type='negative')
    
    def import_memory(self):
        """Import chat memory."""
        # In a real app, this would open a file dialog
        ui.notify("Import functionality would open file dialog", type='info')
    
    def reset_memory(self):
        """Reset chat memory."""
        try:
            self.ai_agent.clear_memory()
            self.chat_container.clear()
            ui.notify("Memory reset successfully", type='positive')
        except Exception as e:
            ui.notify(f"Reset failed: {e}", type='negative')


def main():
    """Main function to run the integrated demo."""
    app_instance = IntegratedChatApp()
    
    ui.run(
        title='MondrUI + AI Integration Demo',
        favicon='🤖',
        show=True,
        reload=False,
        port=8081
    )


if __name__ == '__main__':
    main()
