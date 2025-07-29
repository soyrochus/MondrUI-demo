#!/usr/bin/env python3
"""
MondrUI Render Test

This script demonstrates the MondrUI rendering system by actually rendering
the bug report form and other components for visual testing.
"""

from nicegui import ui
from mondrui import render_ui, register_action_handler
import json


# Sample action handlers for testing
def handle_bug_report():
    """Handle bug report submission."""
    ui.notify("Bug report submitted!", type='positive')


def handle_chat_resume():
    """Handle chat resume action."""
    ui.notify("Returning to chat...", type='info')


def handle_new_chat():
    """Handle new chat action."""
    ui.notify("Starting new chat...", type='info')


def handle_open_settings():
    """Handle settings action."""
    ui.notify("Opening settings...", type='info')


def handle_search_conversations(query):
    """Handle conversation search."""
    ui.notify(f"Searching for: {query}", type='info')


def handle_send_message(message):
    """Handle sending a message."""
    ui.notify(f"Sending: {message}", type='positive')


# Register action handlers
register_action_handler("bug.report", handle_bug_report)
register_action_handler("chat.resume", handle_chat_resume)
register_action_handler("startNewChat", handle_new_chat)
register_action_handler("openSettings", handle_open_settings)
register_action_handler("searchConversations", handle_search_conversations)
register_action_handler("sendMessage", handle_send_message)


@ui.page('/')
def main():
    """Main page demonstrating MondrUI rendering."""
    
    ui.label('MondrUI Rendering Demo').classes('text-2xl font-bold mb-6')
    
    # Bug Report Form Demo
    ui.label('Bug Report Form Demo').classes('text-xl font-semibold mb-4')
    
    bug_report_spec = {
        "type": "ui.render",
        "component": "bugReportForm",
        "props": {
            "title": "Report a Bug",
            "fields": [
                {"id": "summary", "label": "Bug Summary", "type": "text", "required": True},
                {"id": "description", "label": "Description", "type": "textarea", "required": True},
                {"id": "steps", "label": "Steps to Reproduce", "type": "textarea", "required": False},
                {"id": "severity", "label": "Severity", "type": "select", "options": ["Low", "Medium", "High", "Critical"], "required": True}
            ],
            "actions": [
                {"id": "submit", "label": "Submit", "type": "submit", "target": "bug.report"},
                {"id": "cancel", "label": "Cancel", "type": "cancel", "target": "chat.resume"}
            ]
        }
    }
    
    # Render the bug report form
    try:
        render_ui(bug_report_spec)
    except Exception as e:
        ui.label(f"Error rendering bug report form: {e}").classes('text-red-500')
    
    ui.separator().classes('my-8')
    
    # Container Demo
    ui.label('Container with Buttons Demo').classes('text-xl font-semibold mb-4')
    
    container_spec = {
        "type": "ui.render",
        "component": "Container",
        "props": {
            "direction": "horizontal",
            "children": [
                {
                    "component": "Button",
                    "props": {
                        "label": "New Chat",
                        "icon": "add",
                        "onClick": "startNewChat"
                    }
                },
                {
                    "component": "Button",
                    "props": {
                        "label": "Settings",
                        "icon": "settings",
                        "onClick": "openSettings"
                    }
                }
            ]
        }
    }
    
    try:
        render_ui(container_spec)
    except Exception as e:
        ui.label(f"Error rendering container: {e}").classes('text-red-500')
    
    ui.separator().classes('my-8')
    
    # Header Demo
    ui.label('Header Demo').classes('text-xl font-semibold mb-4')
    
    header_spec = {
        "type": "ui.render",
        "component": "Header",
        "props": {
            "title": "MondrUI Chat",
            "actions": [
                {"icon": "settings", "action": "openSettings"}
            ]
        }
    }
    
    try:
        render_ui(header_spec)
    except Exception as e:
        ui.label(f"Error rendering header: {e}").classes('text-red-500')
    
    ui.separator().classes('my-8')
    
    # Chat Input Demo
    ui.label('Chat Input Demo').classes('text-xl font-semibold mb-4')
    
    chat_input_spec = {
        "type": "ui.render",
        "component": "ChatInput",
        "props": {
            "onSend": "sendMessage",
            "placeholder": "Type your message..."
        }
    }
    
    try:
        render_ui(chat_input_spec)
    except Exception as e:
        ui.label(f"Error rendering chat input: {e}").classes('text-red-500')
    
    ui.separator().classes('my-8')
    
    # JSON Display
    ui.label('JSON Specifications Used').classes('text-xl font-semibold mb-4')
    
    with ui.expansion('Bug Report Form JSON', icon='code'):
        ui.code(json.dumps(bug_report_spec, indent=2)).classes('text-xs')
    
    with ui.expansion('Container JSON', icon='code'):
        ui.code(json.dumps(container_spec, indent=2)).classes('text-xs')
    
    with ui.expansion('Header JSON', icon='code'):
        ui.code(json.dumps(header_spec, indent=2)).classes('text-xs')
    
    with ui.expansion('Chat Input JSON', icon='code'):
        ui.code(json.dumps(chat_input_spec, indent=2)).classes('text-xs')


@ui.page('/chatgpt-demo')
def chatgpt_demo():
    """Demo page showing a ChatGPT-like interface using MondrUI."""
    
    chatgpt_spec = {
        "type": "ui.render",
        "component": "Container",
        "props": {
            "direction": "vertical",
            "children": [
                {
                    "component": "Header",
                    "props": {
                        "title": "MondrUI Chat",
                        "actions": [
                            {"icon": "settings", "action": "openSettings"}
                        ]
                    }
                },
                {
                    "component": "Container",
                    "props": {
                        "direction": "horizontal",
                        "children": [
                            {
                                "component": "Sidebar",
                                "props": {
                                    "direction": "vertical",
                                    "width": "240px",
                                    "children": [
                                        {
                                            "component": "Button",
                                            "props": {
                                                "label": "New Chat",
                                                "icon": "add",
                                                "onClick": "startNewChat"
                                            }
                                        },
                                        {
                                            "component": "Input",
                                            "props": {
                                                "placeholder": "Search chat...",
                                                "onChange": "searchConversations"
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "component": "Container",
                                "props": {
                                    "direction": "vertical",
                                    "grow": True,
                                    "children": [
                                        {
                                            "component": "Divider",
                                            "props": {"margin": "md"}
                                        },
                                        {
                                            "component": "ChatInput",
                                            "props": {
                                                "onSend": "sendMessage",
                                                "placeholder": "Type your message..."
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }
    
    ui.label('ChatGPT-style Interface Demo').classes('text-2xl font-bold mb-6')
    
    try:
        render_ui(chatgpt_spec)
    except Exception as e:
        ui.label(f"Error rendering ChatGPT interface: {e}").classes('text-red-500')
    
    ui.separator().classes('my-8')
    
    with ui.expansion('Full ChatGPT Interface JSON', icon='code'):
        ui.code(json.dumps(chatgpt_spec, indent=2)).classes('text-xs')


if __name__ in {"__main__", "__mp_main__"}:
    # Add some custom CSS for better styling
    ui.add_css('''
        .nicegui-content {
            padding: 2rem;
        }
    ''')
    
    ui.run(title='MondrUI Rendering Demo', port=8081)
