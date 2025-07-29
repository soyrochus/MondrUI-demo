#!/usr/bin/env python3
"""
MondrUI: Dynamic UI Rendering Engine

This module implements the core MondrUI functionality for dynamically
generating NiceGUI component trees from JSON specifications.
"""

from nicegui import ui
from typing import Dict, Any, List, Optional, Callable
import json


class MondrUIRenderer:
    """Core renderer for MondrUI specifications."""
    
    def __init__(self):
        """Initialize the MondrUI renderer with component registry."""
        self.component_registry = {
            'bugReportForm': self._render_bug_report_form,
            'Container': self._render_container,
            'Header': self._render_header,
            'Sidebar': self._render_sidebar,
            'Button': self._render_button,
            'Input': self._render_input,
            'List': self._render_list,
            'ChatHistory': self._render_chat_history,
            'Divider': self._render_divider,
            'ChatInput': self._render_chat_input,
        }
        self.action_handlers = {}
    
    def register_action_handler(self, action: str, handler: Callable):
        """Register a handler for a specific action."""
        self.action_handlers[action] = handler
    
    def render_ui(self, spec: Dict[str, Any]) -> Any:
        """
        Render a UI component tree from a MondrUI specification.
        
        Args:
            spec: The MondrUI JSON specification
            
        Returns:
            The root NiceGUI component
        """
        if spec.get('type') != 'ui.render':
            raise ValueError("Specification must have type 'ui.render'")
        
        component_name = spec.get('component')
        if not component_name:
            raise ValueError("Specification must include a component name")
        
        props = spec.get('props', {})
        
        # Get the renderer for this component
        renderer = self.component_registry.get(component_name)
        if not renderer:
            raise ValueError(f"Unknown component: {component_name}")
        
        return renderer(props)
    
    def _render_bug_report_form(self, props: Dict[str, Any]) -> Any:
        """Render a bug report form template."""
        title = props.get('title', 'Bug Report')
        fields = props.get('fields', [])
        actions = props.get('actions', [])
        
        with ui.card().classes('max-w-md mx-auto p-6') as form_card:
            # Title
            ui.label(title).classes('text-xl font-bold mb-4')
            
            # Form fields
            form_data = {}
            for field in fields:
                field_id = field.get('id', '')
                label = field.get('label', '')
                field_type = field.get('type', 'text')
                required = field.get('required', False)
                options = field.get('options', [])
                
                # Label with required indicator
                label_text = f"{label}{'*' if required else ''}"
                ui.label(label_text).classes('text-sm font-medium mb-1')
                
                # Create appropriate input component
                if field_type == 'text':
                    form_data[field_id] = ui.input().classes('w-full mb-3')
                elif field_type == 'textarea':
                    form_data[field_id] = ui.textarea().classes('w-full mb-3')
                elif field_type == 'select':
                    form_data[field_id] = ui.select(options).classes('w-full mb-3')
                
                # Set required validation
                if required and field_id in form_data:
                    form_data[field_id].props('required')
            
            # Action buttons
            if actions:
                with ui.row().classes('w-full justify-end mt-4 gap-2'):
                    for action in actions:
                        action_id = action.get('id', '')
                        label = action.get('label', '')
                        action_type = action.get('type', 'button')
                        target = action.get('target', '')
                        
                        if action_type == 'submit':
                            btn = ui.button(label).classes('bg-blue-500 text-white')
                        elif action_type == 'cancel':
                            btn = ui.button(label).classes('bg-gray-500 text-white')
                        else:
                            btn = ui.button(label)
                        
                        # Register click handler if target is specified
                        if target and target in self.action_handlers:
                            btn.on('click', lambda t=target: self.action_handlers[t]())
        
        return form_card
    
    def _render_container(self, props: Dict[str, Any]) -> Any:
        """Render a container component."""
        direction = props.get('direction', 'vertical')
        children = props.get('children', [])
        grow = props.get('grow', False)
        width = props.get('width', None)
        
        if direction == 'horizontal':
            container = ui.row()
        else:
            container = ui.column()
        
        if grow:
            container.classes('flex-grow')
        
        if width:
            container.style(f'width: {width}')
        
        # Render children
        with container:
            for child in children:
                self._render_component(child)
        
        return container
    
    def _render_header(self, props: Dict[str, Any]) -> Any:
        """Render a header component."""
        title = props.get('title', '')
        actions = props.get('actions', [])
        
        with ui.header().classes('flex justify-between items-center') as header:
            ui.label(title).classes('text-lg font-bold')
            
            if actions:
                with ui.row():
                    for action in actions:
                        icon = action.get('icon', '')
                        action_name = action.get('action', '')
                        btn = ui.button(icon=icon)
                        if action_name in self.action_handlers:
                            btn.on('click', self.action_handlers[action_name])
        
        return header
    
    def _render_sidebar(self, props: Dict[str, Any]) -> Any:
        """Render a sidebar component."""
        direction = props.get('direction', 'vertical')
        width = props.get('width', '240px')
        children = props.get('children', [])
        
        with ui.column().style(f'width: {width}').classes('bg-gray-100 p-4') as sidebar:
            for child in children:
                self._render_component(child)
        
        return sidebar
    
    def _render_button(self, props: Dict[str, Any]) -> Any:
        """Render a button component."""
        label = props.get('label', '')
        icon = props.get('icon', '')
        on_click = props.get('onClick', '')
        
        btn = ui.button(label, icon=icon if icon else None)
        
        if on_click and on_click in self.action_handlers:
            btn.on('click', self.action_handlers[on_click])
        
        return btn
    
    def _render_input(self, props: Dict[str, Any]) -> Any:
        """Render an input component."""
        placeholder = props.get('placeholder', '')
        on_change = props.get('onChange', '')
        
        input_field = ui.input(placeholder=placeholder)
        
        if on_change and on_change in self.action_handlers:
            input_field.on('change', self.action_handlers[on_change])
        
        return input_field
    
    def _render_list(self, props: Dict[str, Any]) -> Any:
        """Render a list component."""
        data = props.get('data', [])
        item_component = props.get('itemComponent', '')
        empty_message = props.get('emptyMessage', 'No items')
        
        with ui.column() as list_container:
            if not data:
                ui.label(empty_message).classes('text-gray-500 italic')
            else:
                for item in data:
                    # For now, render as simple list items
                    ui.label(str(item))
        
        return list_container
    
    def _render_chat_history(self, props: Dict[str, Any]) -> Any:
        """Render a chat history component."""
        messages = props.get('messages', [])
        
        with ui.column().classes('flex-grow overflow-auto') as chat_container:
            for message in messages:
                ui.chat_message(message.get('text', ''), 
                              name=message.get('name', 'User'),
                              sent=message.get('sent', False))
        
        return chat_container
    
    def _render_divider(self, props: Dict[str, Any]) -> Any:
        """Render a divider component."""
        margin = props.get('margin', 'sm')
        margin_class = f'm-{margin}' if margin else ''
        
        return ui.separator().classes(margin_class)
    
    def _render_chat_input(self, props: Dict[str, Any]) -> Any:
        """Render a chat input component."""
        placeholder = props.get('placeholder', 'Type a message...')
        on_send = props.get('onSend', '')
        
        with ui.row().classes('w-full') as input_row:
            text_input = ui.input(placeholder=placeholder).classes('flex-grow')
            send_btn = ui.button('Send')
            
            if on_send and on_send in self.action_handlers:
                send_btn.on('click', lambda: self.action_handlers[on_send](text_input.value))
                text_input.on('keydown.enter', lambda: self.action_handlers[on_send](text_input.value))
        
        return input_row
    
    def _render_component(self, component_spec: Dict[str, Any]) -> Any:
        """Render a child component from its specification."""
        component_name = component_spec.get('component', '')
        props = component_spec.get('props', {})
        
        renderer = self.component_registry.get(component_name)
        if not renderer:
            # Fallback: render as label with component name
            return ui.label(f"Unknown component: {component_name}")
        
        return renderer(props)


# Global renderer instance
_renderer = MondrUIRenderer()


def render_ui(spec: Dict[str, Any]) -> Any:
    """
    Main function to render a UI component tree from a MondrUI specification.
    
    Args:
        spec: The MondrUI JSON specification
        
    Returns:
        The root NiceGUI component
    """
    return _renderer.render_ui(spec)


def register_action_handler(action: str, handler: Callable):
    """Register a global action handler."""
    _renderer.register_action_handler(action, handler)


def parse_and_render(json_str: str) -> Any:
    """
    Parse a JSON string and render the UI component.
    
    Args:
        json_str: JSON string containing MondrUI specification
        
    Returns:
        The root NiceGUI component
    """
    try:
        spec = json.loads(json_str)
        return render_ui(spec)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
