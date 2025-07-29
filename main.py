#!/usr/bin/env python3
from ai import AIAgent
from log_callback_handler import NiceGuiLogElementCallbackHandler
from dotenv import load_dotenv
from nicegui import ui
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


@ui.page('/')
def main():
    ai_agent = AIAgent(model='gpt-4o-mini')

    async def send() -> None:
        question = text.value
        text.value = ''

        with message_container:
            ui.chat_message(text=question, name='You', sent=True)
            response_message = ui.chat_message(name='Bot', sent=False)
            spinner = ui.spinner(type='dots')

        response = ''
        async for chunk in ai_agent.send_message(question, NiceGuiLogElementCallbackHandler(log)):
            response += chunk
            response_message.clear()
            with response_message:
                ui.html(response)
            ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        message_container.remove(spinner)

    async def new_chat() -> None:
        """Start a new conversation by clearing memory."""
        ai_agent.clear_memory()
        message_container.clear()
        with message_container:
            ui.markdown("*Conversation cleared. Starting fresh!*").classes('text-gray-500 italic')

    ui.add_css(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}')

    # the queries below are used to expand the contend down to the footer (content can then use flex-grow to expand)
    ui.query('.q-page').classes('flex')
    ui.query('.nicegui-content').classes('w-full')

    with ui.tabs().classes('w-full') as tabs:
        chat_tab = ui.tab('Chat')
        logs_tab = ui.tab('Logs')
        memory_tab = ui.tab('Memory')
    with ui.tab_panels(tabs, value=chat_tab).classes('w-full max-w-2xl mx-auto flex-grow items-stretch'):
        message_container = ui.tab_panel(chat_tab).classes('items-stretch')
        with ui.tab_panel(logs_tab):
            log = ui.log().classes('w-full h-full')
        with ui.tab_panel(memory_tab).classes('p-4'):
            ui.label('Conversation Memory').classes('text-lg font-bold mb-4')
            memory_display = ui.column().classes('w-full')
            
            def update_memory_display():
                memory_display.clear()
                with memory_display:
                    messages = ai_agent.get_conversation_history()
                    stats = ai_agent.get_memory_stats()
                    
                    if not messages:
                        ui.label('No conversation history').classes('text-gray-500 italic')
                    else:
                        # Display memory statistics
                        with ui.card().classes('mb-4 p-3 bg-blue-50'):
                            ui.label('Memory Statistics').classes('font-bold text-sm mb-2')
                            ui.label(f'Conversation turns: {stats["conversation_turns"]}').classes('text-sm')
                            ui.label(f'Total messages: {stats["total_messages"]} / {stats["max_messages"]}').classes('text-sm')
                            ui.label(f'Memory usage: {stats["memory_usage_percent"]:.1f}%').classes('text-sm')
                        
                        # Display conversation history
                        ui.label('Conversation History:').classes('font-bold text-sm mb-2')
                        for i, msg in enumerate(messages):
                            with ui.card().classes('mb-2 p-3'):
                                # Check message type using isinstance
                                from ai import HumanMessage
                                msg_type = "Human" if isinstance(msg, HumanMessage) else "AI"
                                timestamp = f"Message {i+1}"
                                ui.label(f'{timestamp} - {msg_type}:').classes('font-bold text-sm text-blue-600')
                                ui.markdown(str(msg.content)).classes('mt-1')
            
            ui.button('Refresh Memory View', on_click=update_memory_display).classes('mb-4')
            ui.button('Clear Conversation', on_click=new_chat).classes('mb-4 bg-red-500')

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            ui.button('New Chat', on_click=new_chat).classes('mr-2').props('flat color=primary')
            placeholder = 'message' if OPENAI_API_KEY != 'not-set' else \
                'Please provide your OPENAI key in the Python script first!'
            text = ui.input(placeholder=placeholder).props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
        ui.markdown('MondrUI demo with conversational memory - built with [NiceGUI](https://nicegui.io)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')


ui.run(title='MondrUI Demo - Conversational AI with Memory')