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


def setup_form_handlers(ai_agent: AIAgent, message_container, log_element):
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
    
    def create_data_collector(field_id):
        """Create a data collector function for a specific field"""
        def collector(value):
            print(f"Data collector called: field_id={field_id}, value={value}")
            if 'current_form' not in form_data_store:
                form_data_store['current_form'] = {}
            form_data_store['current_form'][field_id] = value
            print(f"Form data store updated: {form_data_store['current_form']}")
        return collector
    
    # Register common form actions
    register_action_handler("submit_bug", create_form_handler("submit_bug", "Bug Report"))
    register_action_handler("submit_help", create_form_handler("submit_help", "Help Request"))
    register_action_handler("submit_feedback", create_form_handler("submit_feedback", "Feedback"))
    register_action_handler("submit_form", create_form_handler("submit_form", "Form"))
    
    # Return both the data collector factory and form data store for use in form rendering
    return create_data_collector, form_data_store


@ui.page('/')
def main():
    ai_agent = AIAgent(model='gpt-4o-mini')

    def render_any_form_with_data_collection(props: dict, data_collector_factory):
        """Render any form with data collection, works for all form types."""
        title = props.get('title', 'Form')
        fields = props.get('fields', [])
        
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
                elif field_type == 'number':
                    ui.number(
                        placeholder=f'Enter {field_label.lower()}...',
                        on_change=lambda e, collector=collector: collector(e.value)
                    ).classes('w-full')
                elif field_type == 'email':
                    ui.input(
                        placeholder=f'Enter {field_label.lower()}...',
                        on_change=lambda e, collector=collector: collector(e.value)
                    ).classes('w-full').props('type=email')
                elif field_type == 'radio':
                    # Radio button group for exclusive selection
                    options = field.get('options', {})
                    value = field.get('value')
                    inline = field.get('inline', False)
                    
                    radio = ui.radio(options, value=value)
                    if inline:
                        radio.props('inline')
                    
                    def create_radio_handler(collector):
                        def on_radio_change():
                            current_value = radio.value
                            log.push(f"Radio changed: {current_value}")
                            collector(current_value)
                        return on_radio_change
                    
                    radio.on('update:model-value', create_radio_handler(collector))
                    
                elif field_type == 'checkboxGroup':
                    # Checkbox group for multiple selections
                    options = field.get('options', {})
                    selected_values = field.get('value', [])
                    layout = field.get('layout', 'vertical')
                    
                    if layout == 'horizontal':
                        container = ui.row()
                    else:
                        container = ui.column()
                    
                    current_selections = set(selected_values) if selected_values else set()
                    
                    with container:
                        for option_value, option_label in options.items():
                            checkbox = ui.checkbox(
                                text=option_label,
                                value=option_value in current_selections
                            )
                            
                            def create_checkbox_handler(val, collector):
                                def on_checkbox_change():
                                    current_value = checkbox.value
                                    if current_value:
                                        current_selections.add(val)
                                    else:
                                        current_selections.discard(val)
                                    log.push(f"Checkbox changed: {list(current_selections)}")
                                    collector(list(current_selections))
                                return on_checkbox_change
                            
                            checkbox.on('update:model-value', create_checkbox_handler(option_value, collector))
                
                elif field_type == 'slider':
                    # Range slider for value selection
                    min_val = field.get('min', 0)
                    max_val = field.get('max', 100)
                    step = field.get('step', 1)
                    value = field.get('value', min_val)
                    min_label = field.get('minLabel')
                    max_label = field.get('maxLabel')
                    show_value = field.get('showValue', True)
                    label_always = field.get('labelAlways', False)
                    
                    with ui.column().classes('w-full'):
                        # Scale labels if provided
                        if min_label and max_label:
                            with ui.row().classes('w-full justify-between text-sm text-gray-600'):
                                ui.label(min_label)
                                ui.label(max_label)
                        
                        # The slider itself
                        slider = ui.slider(min=min_val, max=max_val, step=step, value=value)
                        
                        if label_always:
                            slider.props('label-always')
                        
                        # Value display
                        if show_value:
                            value_label = ui.label(f'Value: {value}').classes('text-center text-sm')
                        
                        # Set up event handling using direct callback binding
                        def handle_slider_change():
                            current_value = slider.value
                            log.push(f"Slider changed: {current_value}")
                            collector(current_value)
                            if show_value:
                                value_label.text = f'Value: {current_value}'
                        
                        slider.on('update:model-value', handle_slider_change)
                
                else:  # text input (default)
                    ui.input(
                        placeholder=f'Enter {field_label.lower()}...',
                        on_change=lambda e, collector=collector: collector(e.value)
                    ).classes('w-full')

    # Note: The render_custom_bug_form function has been replaced by render_any_form_with_data_collection

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
            log.push(f"MondrUI JSON detected: {mondrui_spec}")
            
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
                        # Log form rendering attempt
                        log.push(f"Attempting to render MondrUI form: {mondrui_spec}")
                        
                        # Use unified form renderer with data collection for ALL form types
                        # This ensures consistent behavior and data collection
                        form_props = mondrui_spec.get('props', {})
                        render_any_form_with_data_collection(form_props, data_collector_factory)
                        
                        log.push("Form rendered successfully")
                        
                        # Unified submit & close button that sends all data to AI
                        async def handle_submit_and_close():
                            # Get collected form data
                            collected_data = form_data_store.get('current_form', {})
                            log.push(f"Form submission: collected_data = {collected_data}")
                            
                            # Only send data if there's actually some data collected
                            if collected_data:
                                # Determine form type from the MondrUI spec
                                form_title = mondrui_spec.get('props', {}).get('title', 'Form')
                                action_name = 'submit_form'  # Default action
                                if mondrui_spec.get('component') == 'bugReportForm':
                                    action_name = 'submit_bug'
                                
                                collected_data['action'] = action_name
                                collected_data['timestamp'] = '2025-01-01T00:00:00Z'  # In real app, use datetime.now()
                                
                                # Close the dialog first
                                form_dialog.close()
                                
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
                                async for chunk in ai_agent.send_message(form_message, NiceGuiLogElementCallbackHandler(log)):
                                    response += chunk
                                    response_message.clear()
                                    with response_message:
                                        ui.html(response)
                                    ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
                                message_container.remove(spinner)
                                
                                # Clear form data after submission
                                form_data_store['current_form'] = {}
                            else:
                                # No data collected, just close
                                form_dialog.close()
                                with message_container:
                                    ui.chat_message(
                                        text="Form was closed without submitting any data.", 
                                        name='System', 
                                        sent=False
                                    ).classes('bg-gray-50')
                        
                        ui.button('Submit & Close', on_click=handle_submit_and_close).classes('mt-4 bg-blue-500 text-white')
                        
                    except Exception as e:
                        error_msg = f'Error rendering form: {str(e)}'
                        log.push(f"FORM RENDERING ERROR: {error_msg}")
                        log.push(f"MondrUI spec: {mondrui_spec}")
                        log.push(f"Exception type: {type(e).__name__}")
                        import traceback
                        log.push(f"Traceback: {traceback.format_exc()}")
                        
                        ui.label(error_msg).classes('text-red-500')
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

    # Set up form handlers for MondrUI forms (after log element is created)
    data_collector_factory, form_data_store = setup_form_handlers(ai_agent, message_container, log)
    
    # Add a startup log message to verify logging is working
    log.push("MondrUI application started - logging is active")

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