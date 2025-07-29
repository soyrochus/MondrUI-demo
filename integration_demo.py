#!/usr/bin/env python3
"""
Integration test showing how MondrUI can be used with the AI agent.
"""

from ai import AIAgent
from mondrui import render_ui, register_action_handler
from nicegui import ui
import json


# Example of how the AI could generate MondrUI specifications
def ai_generate_bug_form():
    """Simulate AI generating a bug report form specification."""
    return {
        "type": "ui.render",
        "component": "bugReportForm",
        "props": {
            "title": "AI-Generated Bug Report",
            "fields": [
                {"id": "summary", "label": "Bug Summary", "type": "text", "required": True},
                {"id": "description", "label": "Description", "type": "textarea", "required": True},
                {"id": "severity", "label": "Severity", "type": "select", "options": ["Low", "Medium", "High", "Critical"], "required": True}
            ],
            "actions": [
                {"id": "submit", "label": "Submit Bug", "type": "submit", "target": "bug.submit"},
                {"id": "cancel", "label": "Cancel", "type": "cancel", "target": "chat.resume"}
            ]
        }
    }


@ui.page('/')
def integration_demo():
    """Demo showing AI + MondrUI integration."""
    
    ui.label('MondrUI + AI Integration Demo').classes('text-2xl font-bold mb-6')
    
    # Create AI agent
    ai_agent = AIAgent()
    
    # Action handlers
    def handle_bug_submit():
        ui.notify("Bug submitted via AI-generated form!", type='positive')
    
    def handle_chat_resume():
        ui.notify("Returning to AI chat...", type='info')
    
    register_action_handler("bug.submit", handle_bug_submit)
    register_action_handler("chat.resume", handle_chat_resume)
    
    # Demo buttons
    with ui.row().classes('mb-6 gap-4'):
        ui.button('Generate Bug Form (AI)', 
                 on_click=lambda: generate_and_render_form()).classes('bg-blue-500')
        ui.button('Show JSON Spec', 
                 on_click=lambda: show_json_spec()).classes('bg-green-500')
        ui.button('Clear Forms', 
                 on_click=lambda: clear_forms()).classes('bg-red-500')
    
    # Container for dynamically generated forms
    global form_container
    form_container = ui.column().classes('w-full')
    
    # Container for JSON display
    global json_container
    json_container = ui.column().classes('w-full')
    
    def generate_and_render_form():
        """Generate and render a form using AI logic."""
        form_container.clear()
        json_container.clear()
        
        with form_container:
            ui.label('AI-Generated Form:').classes('text-lg font-semibold mb-4')
            
            # Simulate AI generating the form specification
            form_spec = ai_generate_bug_form()
            
            try:
                # Render the form using MondrUI
                render_ui(form_spec)
                ui.notify("Form generated successfully!", type='positive')
            except Exception as e:
                ui.label(f"Error rendering form: {e}").classes('text-red-500')
    
    def show_json_spec():
        """Show the JSON specification."""
        json_container.clear()
        
        with json_container:
            ui.label('Generated JSON Specification:').classes('text-lg font-semibold mb-4')
            form_spec = ai_generate_bug_form()
            ui.code(json.dumps(form_spec, indent=2)).classes('text-xs bg-gray-100 p-4 rounded')
    
    def clear_forms():
        """Clear all generated content."""
        form_container.clear()
        json_container.clear()
        ui.notify("Content cleared", type='info')
    
    # Add information about the integration
    ui.separator().classes('my-8')
    
    with ui.card().classes('p-6 bg-blue-50'):
        ui.label('How MondrUI + AI Integration Works:').classes('text-lg font-bold mb-4')
        
        with ui.column().classes('gap-2'):
            ui.label('1. User sends a message like "I want to report a bug"')
            ui.label('2. AI Agent analyzes the intent and decides to show a form')
            ui.label('3. AI generates a MondrUI JSON specification for a bug report form')
            ui.label('4. MondrUI renderer creates the actual UI components')
            ui.label('5. User interacts with the form, data is processed')
            ui.label('6. Conversation continues seamlessly')
    
    # Show example AI conversation flow
    ui.separator().classes('my-8')
    
    ui.label('Example AI Conversation Flow:').classes('text-lg font-semibold mb-4')
    
    with ui.column().classes('gap-2 bg-gray-50 p-4 rounded'):
        ui.markdown('**User:** "I found a bug in the application"')
        ui.markdown('**AI:** "I\'ll help you report that bug. Let me create a form for you."')
        ui.markdown('**AI:** *[Generates MondrUI specification and renders bug form]*')
        ui.markdown('**AI:** "Please fill out the form above and I\'ll submit the bug report."')
        ui.markdown('**User:** *[Fills form and submits]*')
        ui.markdown('**AI:** "Bug report submitted successfully! Is there anything else I can help with?"')


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='MondrUI + AI Integration Demo', port=8082)
