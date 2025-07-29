#!/usr/bin/env python3
"""
MondrUI visual demos and examples.
This module demonstrates the generic MondrUI rendering capabilities.
"""

import asyncio
from nicegui import ui, app
from mondrui import render_ui


def setup_bug_report_demo():
    """Set up the bug report form demo."""
    
    # Bug report form specification
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
                {"id": "submit", "label": "Submit Bug Report", "action": "submit_bug"},
                {"id": "cancel", "label": "Cancel", "action": "cancel_bug"}
            ]
        }
    }
    
    with ui.card().classes('w-full max-w-4xl mx-auto'):
        ui.label('MondrUI Demo: Bug Report Form').classes('text-2xl font-bold mb-4')
        
        # Render the bug report form using MondrUI
        try:
            rendered_form = render_ui(bug_report_spec)
            ui.label('✅ Bug report form rendered successfully!').classes('text-green-600 mb-4')
        except Exception as e:
            ui.label(f'❌ Error rendering form: {str(e)}').classes('text-red-600')


def setup_component_showcase():
    """Set up the component showcase demo."""
    
    with ui.card().classes('w-full max-w-4xl mx-auto mt-8'):
        ui.label('MondrUI Component Showcase').classes('text-2xl font-bold mb-4')
        
        # Text component demo
        text_spec = {
            "type": "ui.render",
            "component": "Text",
            "props": {
                "text": "Welcome to MondrUI!",
                "variant": "h2",
                "style": {"classes": ["text-blue-600", "mb-4"]}
            }
        }
        
        try:
            render_ui(text_spec)
            ui.label('✅ Text component rendered').classes('text-green-600 text-sm')
        except Exception as e:
            ui.label(f'❌ Text component error: {str(e)}').classes('text-red-600 text-sm')
        
        ui.separator()
        
        # Container with multiple children
        container_spec = {
            "type": "ui.render",
            "component": "Container",
            "props": {
                "layout": "horizontal",
                "style": {"classes": ["gap-4", "mt-4"]},
                "children": [
                    {
                        "component": "Button",
                        "props": {
                            "label": "Primary Action",
                            "variant": "primary",
                            "icon": "star"
                        }
                    },
                    {
                        "component": "Button",
                        "props": {
                            "label": "Secondary Action",
                            "variant": "secondary",
                            "icon": "settings"
                        }
                    }
                ]
            }
        }
        
        try:
            render_ui(container_spec)
            ui.label('✅ Container with buttons rendered').classes('text-green-600 text-sm')
        except Exception as e:
            ui.label(f'❌ Container error: {str(e)}').classes('text-red-600 text-sm')


def setup_chat_interface_demo():
    """Set up a chat interface demo using MondrUI."""
    
    with ui.card().classes('w-full max-w-4xl mx-auto mt-8'):
        ui.label('MondrUI Chat Interface Demo').classes('text-2xl font-bold mb-4')
        
        # Chat container spec
        chat_spec = {
            "type": "ui.render",
            "component": "Container",
            "props": {
                "layout": "vertical",
                "style": {"classes": ["h-96", "border", "rounded-lg", "p-4"]},
                "children": [
                    {
                        "component": "Container",
                        "props": {
                            "layout": "vertical",
                            "style": {"classes": ["flex-1", "overflow-auto", "mb-4"]},
                            "children": [
                                {
                                    "component": "Text",
                                    "props": {
                                        "text": "User: Hello, how can I report a bug?",
                                        "style": {"classes": ["mb-2", "p-2", "bg-blue-100", "rounded"]}
                                    }
                                },
                                {
                                    "component": "Text",
                                    "props": {
                                        "text": "Assistant: I can help you create a bug report form. Let me render one for you using MondrUI!",
                                        "style": {"classes": ["mb-2", "p-2", "bg-gray-100", "rounded"]}
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "component": "Container",
                        "props": {
                            "layout": "horizontal",
                            "style": {"classes": ["gap-2"]},
                            "children": [
                                {
                                    "component": "Input",
                                    "props": {
                                        "inputType": "text",
                                        "placeholder": "Type your message...",
                                        "style": {"classes": ["flex-1"]}
                                    }
                                },
                                {
                                    "component": "Button",
                                    "props": {
                                        "label": "Send",
                                        "variant": "primary",
                                        "icon": "send"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
        
        try:
            render_ui(chat_spec)
            ui.label('✅ Chat interface rendered').classes('text-green-600 text-sm')
        except Exception as e:
            ui.label(f'❌ Chat interface error: {str(e)}').classes('text-red-600 text-sm')


async def main():
    """Main function to set up all demos."""
    
    # Set up the page
    ui.query('.nicegui-content').classes('p-8')
    
    with ui.column().classes('w-full max-w-6xl mx-auto'):
        ui.label('MondrUI Generic Rendering System').classes('text-4xl font-bold text-center mb-8')
        ui.label('Demonstrating dynamic UI generation from JSON specifications').classes('text-xl text-center text-gray-600 mb-8')
        
        # Set up all demo sections
        setup_bug_report_demo()
        setup_component_showcase()
        setup_chat_interface_demo()
        
        # Add some documentation
        with ui.card().classes('w-full max-w-4xl mx-auto mt-8'):
            ui.label('About MondrUI').classes('text-2xl font-bold mb-4')
            ui.markdown("""
MondrUI is a generic UI rendering system that allows you to create dynamic user interfaces 
from JSON specifications. Key features:

- **Generic Component System**: Extensible architecture with abstract base components
- **Template System**: Reusable UI templates with variable substitution
- **Plugin Architecture**: Easy registration of custom components and templates
- **Event Handling**: Unified event system with action handlers
- **Style Management**: Flexible styling with CSS classes and inline styles
- **NiceGUI Integration**: Seamless integration with NiceGUI for web UIs

The system supports various component types including containers, forms, buttons, 
inputs, text elements, and custom components that you can define and register.
            """)


if __name__ == '__main__':
    ui.run(
        title='MondrUI Demo',
        favicon='🎨',
        show=True,
        reload=False,
        port=8080
    )
