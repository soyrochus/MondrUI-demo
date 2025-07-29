#!/usr/bin/env python3
from ai import AIAgent
from log_callback_handler import NiceGuiLogElementCallbackHandler
from dotenv import load_dotenv
from nicegui import ui
from mondrui import render_ui, register_action_handler
import os
import json
import re

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def extract_mondrui_json(text: str) -> tuple[str, dict | None]:
    """
    Extract MondrUI JSON from AI response text.
    Returns (cleaned_text, json_spec) where json_spec is None if no valid JSON found.
    """
    # Look for JSON code blocks that contain MondrUI specifications
    json_pattern = r'```json\s*(\{[^`]*"type":\s*"ui\.render"[^`]*\})\s*```'
    match = re.search(json_pattern, text, re.DOTALL)
    
    if not match:
        return text, None
    
    try:
        json_str = match.group(1)
        json_spec = json.loads(json_str)
        
        # Validate it's a proper MondrUI spec
        if json_spec.get("type") == "ui.render" and "component" in json_spec:
            # Remove the JSON block from the text
            cleaned_text = re.sub(json_pattern, "", text, flags=re.DOTALL).strip()
            return cleaned_text, json_spec
    except json.JSONDecodeError:
        pass
    
    return text, None


def setup_form_handlers(ai_agent: AIAgent, message_container):
    """Set up form action handlers for MondrUI forms."""
    
    # Store form data globally so handlers can access it
    form_data_store = {}
    
    async def handle_form_submission(action_name: str, form_title: str = "Form"):
        """Handle form submission and send data back to AI."""
        
        # Get collected form data
        collected_data = form_data_store.get('current_form', {})
        collected_data['action'] = action_name
        collected_data['timestamp'] = '2025-01-01T00:00:00Z'  # In real app, use datetime.now()
        
        # Add form submission message to chat
        with message_container:
            ui.chat_message(
                text=f"✅ {form_title} submitted with data: {json.dumps(collected_data, indent=2)}", 
                name='System', 
                sent=False
            ).classes('bg-green-50')
            
            # Get AI response about the submitted data
            response_message = ui.chat_message(name='Bot', sent=False)
            spinner = ui.spinner(type='dots')

        # Send form data to AI for processing
        form_message = f"User submitted form data: {json.dumps(collected_data, indent=2)}. Please acknowledge receipt and process this information."
        
        response = ''
        async for chunk in ai_agent.send_message(form_message):
            response += chunk
            response_message.clear()
            with response_message:
                ui.html(response)
            ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        message_container.remove(spinner)
        
        # Clear form data after submission
        form_data_store['current_form'] = {}
    
    def create_form_handler(action_name: str, form_title: str = "Form"):
        async def handler():
            await handle_form_submission(action_name, form_title)
        return handler
    
    def create_data_collector(field_id: str):
        """Create a data collector function for a specific field."""
        def collect_data(value):
            if 'current_form' not in form_data_store:
                form_data_store['current_form'] = {}
            form_data_store['current_form'][field_id] = value
        return collect_data
    
    # Register common form actions
    register_action_handler("submit_bug", create_form_handler("submit_bug", "Bug Report"))
    register_action_handler("submit_help", create_form_handler("submit_help", "Help Request"))
    register_action_handler("submit_feedback", create_form_handler("submit_feedback", "Feedback"))
    register_action_handler("submit_form", create_form_handler("submit_form", "Form"))
    
    # Return the data collector factory for use in form rendering
    return create_data_collector


@ui.page('/')
def main():
    ai_agent = AIAgent(model='gpt-4o-mini')

    def render_custom_bug_form(props: dict, data_collector_factory):
        """Render a custom bug report form with data collection."""
        title = props.get('title', 'Bug Report')
        fields = props.get('fields', [])
        actions = props.get('actions', [])
        
        ui.label(title).classes('text-lg font-bold mb-4')
        
        # Create input fields with data collection
        with ui.column().classes('gap-4 w-full'):
            for field in fields:
                field_id = field.get('id', '')
                field_label = field.get('label', '')
                field_type = field.get('type', 'text')
                required = field.get('required', False)
                
                label_text = field_label + (' *' if required else '')
                ui.label(label_text).classes('font-medium')
                
                collector = data_collector_factory(field_id)
                
                if field_type == 'textarea':
                    ui.textarea(
                        placeholder=f'Enter {field_label.lower()}...',
                        on_change=lambda e, collector=collector: collector(e.value)
                    ).classes('w-full')
                elif field_type == 'select':
                    options = field.get('options', [])
                    ui.select(
                        options=options,
                        on_change=lambda e, collector=collector: collector(e.value)
                    ).classes('w-full')
                else:  # text input
                    ui.input(
                        placeholder=f'Enter {field_label.lower()}...',
                        on_change=lambda e, collector=collector: collector(e.value)
                    ).classes('w-full')
            
            # Render action buttons
            if actions:
                with ui.row().classes('w-full justify-end mt-4 gap-2'):
                    for action in actions:
                        label = action.get('label', 'Submit')
                        action_name = action.get('action', 'submit_form')
                        
                        async def handle_action(action_name=action_name):
                            # Trigger the registered action handler
                            try:
                                from mondrui import MondrUIRenderer
                                renderer = MondrUIRenderer()
                                handler = renderer.action_handlers.get(action_name)
                                if handler:
                                    await handler()
                            except Exception as e:
                                ui.notify(f'Action error: {e}', type='negative')
                        
                        ui.button(label, on_click=handle_action).classes('bg-blue-500 text-white')

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
        
        # Check if response contains MondrUI JSON and render form if found
        cleaned_response, mondrui_spec = extract_mondrui_json(response)
        
        if mondrui_spec:
            # Update the response message with cleaned text
            response_message.clear()
            with response_message:
                if cleaned_response.strip():
                    ui.html(cleaned_response)
                else:
                    ui.html("I've prepared a form for you:")
            
            # Render the MondrUI form in a dialog
            with ui.dialog() as form_dialog:
                with ui.card().classes('w-full max-w-2xl'):
                    ui.label('📋 Interactive Form').classes('text-lg font-bold mb-4')
                    
                    try:
                        # Create a custom form renderer with data collection
                        if mondrui_spec.get('component') == 'bugReportForm':
                            render_custom_bug_form(mondrui_spec.get('props', {}), data_collector_factory)
                        else:
                            # Fallback to standard MondrUI rendering
                            render_ui(mondrui_spec)
                        
                        # Add close button
                        ui.button('Close Form', on_click=form_dialog.close).classes('mt-4')
                        
                    except Exception as e:
                        ui.label(f'Error rendering form: {str(e)}').classes('text-red-500')
                        ui.button('Close', on_click=form_dialog.close)
            
            # Open the form dialog
            form_dialog.open()

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
                                from langchain_core.messages import HumanMessage
                                msg_type = "Human" if isinstance(msg, HumanMessage) else "AI"
                                timestamp = f"Message {i+1}"
                                ui.label(f'{timestamp} - {msg_type}:').classes('font-bold text-sm text-blue-600')
                                ui.markdown(str(msg.content)).classes('mt-1')
            
            ui.button('Refresh Memory View', on_click=update_memory_display).classes('mb-4')
            ui.button('Clear Conversation', on_click=new_chat).classes('mb-4 bg-red-500')

    # Set up form handlers for MondrUI forms
    data_collector_factory = setup_form_handlers(ai_agent, message_container)

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