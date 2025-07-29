#!/usr/bin/env python3
"""
MondrUI: Truly Generic Dynamic UI Rendering Engine

This module implements a generic, extensible UI rendering system that can
dynamically generate NiceGUI component trees from JSON specifications.
"""

from nicegui import ui
from typing import Dict, Any, List, Optional, Callable, Type, Union
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class LayoutType(Enum):
    """Standard layout types."""
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    GRID = "grid"
    FLEX = "flex"


class EventType(Enum):
    """Standard event types."""
    CLICK = "click"
    CHANGE = "change"
    SUBMIT = "submit"
    KEYDOWN = "keydown"
    FOCUS = "focus"
    BLUR = "blur"
    SLIDE = "slide"  # For slider components


@dataclass
class ComponentStyle:
    """Standardized styling properties."""
    classes: List[str] = field(default_factory=list)
    width: Optional[str] = None
    height: Optional[str] = None
    padding: Optional[str] = None
    margin: Optional[str] = None
    background: Optional[str] = None
    color: Optional[str] = None
    border: Optional[str] = None
    
    def apply_to_element(self, element) -> None:
        """Apply styles to a NiceGUI element."""
        if self.classes:
            element.classes(' '.join(self.classes))
        
        style_dict = {}
        if self.width: style_dict['width'] = self.width
        if self.height: style_dict['height'] = self.height
        if self.padding: style_dict['padding'] = self.padding
        if self.margin: style_dict['margin'] = self.margin
        if self.background: style_dict['background'] = self.background
        if self.color: style_dict['color'] = self.color
        if self.border: style_dict['border'] = self.border
        
        if style_dict:
            element.style(style_dict)


@dataclass
class EventHandler:
    """Standardized event handling."""
    event: EventType
    action: str
    params: Dict[str, Any] = field(default_factory=dict)


class BaseComponent(ABC):
    """Abstract base class for all MondrUI components."""
    
    def __init__(self, component_type: str, props: Dict[str, Any]):
        self.type = component_type
        self.props = props
        self.style = self._parse_style(props.get('style', {}))
        self.events = self._parse_events(props.get('events', {}))
        self.children = props.get('children', [])
        
    def _parse_style(self, style_props: Dict[str, Any]) -> ComponentStyle:
        """Parse style properties into ComponentStyle object."""
        return ComponentStyle(
            classes=style_props.get('classes', []),
            width=style_props.get('width'),
            height=style_props.get('height'),
            padding=style_props.get('padding'),
            margin=style_props.get('margin'),
            background=style_props.get('background'),
            color=style_props.get('color'),
            border=style_props.get('border')
        )
    
    def _parse_events(self, event_props: Dict[str, Any]) -> List[EventHandler]:
        """Parse event properties into EventHandler objects."""
        events = []
        for event_name, action in event_props.items():
            try:
                event_type = EventType(event_name.lower())
                if isinstance(action, str):
                    events.append(EventHandler(event_type, action))
                elif isinstance(action, dict):
                    events.append(EventHandler(
                        event_type, 
                        action.get('action', ''),
                        action.get('params', {})
                    ))
            except ValueError:
                # Skip unknown event types
                pass
        return events
    
    @abstractmethod
    def render(self, renderer: 'MondrUIRenderer') -> Any:
        """Render the component and return the NiceGUI element."""
        pass
    
    def validate_props(self) -> bool:
        """Validate component properties. Override in subclasses."""
        return True
    
    def apply_styling_and_events(self, element: Any, renderer: 'MondrUIRenderer') -> None:
        """Apply styling and event handlers to the rendered element."""
        self.style.apply_to_element(element)
        
        for event in self.events:
            if event.action in renderer.action_handlers:
                handler = renderer.action_handlers[event.action]
                
                if event.event == EventType.CLICK:
                    element.on('click', lambda h=handler, p=event.params: h(**p))
                elif event.event == EventType.CHANGE:
                    element.on('change', lambda h=handler, p=event.params: h(element.value, **p))
                elif event.event == EventType.SUBMIT:
                    element.on('submit', lambda h=handler, p=event.params: h(**p))
                elif event.event == EventType.SLIDE:
                    element.on('update:model-value', lambda h=handler, p=event.params: h(element.value, **p))
                # Add more event types as needed


class ContainerComponent(BaseComponent):
    """Generic container component with flexible layout."""
    
    def render(self, renderer: 'MondrUIRenderer') -> Any:
        layout = self.props.get('layout', LayoutType.VERTICAL.value)
        
        if layout == LayoutType.HORIZONTAL.value:
            container = ui.row()
        elif layout == LayoutType.GRID.value:
            container = ui.grid(columns=self.props.get('columns', 2))
        else:  # Default to vertical
            container = ui.column()
        
        self.apply_styling_and_events(container, renderer)
        
        # Render children
        with container:
            for child_spec in self.children:
                renderer.render_component(child_spec)
        
        return container


class TextComponent(BaseComponent):
    """Generic text component (labels, headings, etc.)."""
    
    def render(self, renderer: 'MondrUIRenderer') -> Any:
        text = self.props.get('text', '')
        variant = self.props.get('variant', 'body')  # body, h1, h2, h3, caption
        
        if variant.startswith('h'):
            element = ui.html(f'<{variant}>{text}</{variant}>')
        elif variant == 'caption':
            element = ui.label(text).classes('text-sm text-gray-500')
        else:
            element = ui.label(text)
        
        self.apply_styling_and_events(element, renderer)
        return element


class InputComponent(BaseComponent):
    """Generic input component supporting various input types."""
    
    def render(self, renderer: 'MondrUIRenderer') -> Any:
        input_type = self.props.get('inputType', 'text')
        placeholder = self.props.get('placeholder', '')
        value = self.props.get('value', '')
        required = self.props.get('required', False)
        options = self.props.get('options', [])
        
        if input_type == 'textarea':
            element = ui.textarea(value=value, placeholder=placeholder)
        elif input_type == 'select':
            element = ui.select(options=options, value=value)
        elif input_type == 'checkbox':
            element = ui.checkbox(value=bool(value))
        elif input_type == 'number':
            element = ui.number(value=value, placeholder=placeholder)
        else:  # Default to text
            element = ui.input(value=value, placeholder=placeholder)
        
        if required:
            element.props('required')
        
        self.apply_styling_and_events(element, renderer)
        return element


class ButtonComponent(BaseComponent):
    """Generic button component."""
    
    def render(self, renderer: 'MondrUIRenderer') -> Any:
        label = self.props.get('label', '')
        icon = self.props.get('icon')
        variant = self.props.get('variant', 'default')  # default, primary, secondary, danger
        
        element = ui.button(label, icon=icon)
        
        # Apply variant-specific styling
        if variant == 'primary':
            element.classes('bg-blue-500 text-white')
        elif variant == 'secondary':
            element.classes('bg-gray-500 text-white')
        elif variant == 'danger':
            element.classes('bg-red-500 text-white')
        
        self.apply_styling_and_events(element, renderer)
        return element


class RadioComponent(BaseComponent):
    """Radio button group for exclusive selection."""
    
    def render(self, renderer: 'MondrUIRenderer') -> Any:
        options = self.props.get('options', {})  # {'value': 'label'} format
        value = self.props.get('value')
        field_id = self.props.get('id', '')
        inline = self.props.get('inline', False)
        
        element = ui.radio(options, value=value)
        
        if inline:
            element.props('inline')
        
        self.apply_styling_and_events(element, renderer)
        return element


class CheckboxGroupComponent(BaseComponent):
    """Checkbox group for multiple selections."""
    
    def render(self, renderer: 'MondrUIRenderer') -> Any:
        options = self.props.get('options', {})  # {'value': 'label'} format
        selected_values = self.props.get('value', [])  # List of selected values
        field_id = self.props.get('id', '')
        layout = self.props.get('layout', 'vertical')  # vertical or horizontal
        
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
                
                # Store reference to update selections
                def create_checkbox_handler(val):
                    def on_checkbox_change(e):
                        if e.value:
                            current_selections.add(val)
                        else:
                            current_selections.discard(val)
                    return on_checkbox_change
                
                checkbox.on('change', create_checkbox_handler(option_value))
        
        self.apply_styling_and_events(container, renderer)
        return container


class SliderComponent(BaseComponent):
    """Slider for range value selection."""
    
    def render(self, renderer: 'MondrUIRenderer') -> Any:
        min_val = self.props.get('min', 0)
        max_val = self.props.get('max', 100)
        step = self.props.get('step', 1)
        value = self.props.get('value', min_val)
        field_id = self.props.get('id', '')
        
        # Optional labels for semantic scales
        min_label = self.props.get('minLabel')  # e.g., "Unhappy"
        max_label = self.props.get('maxLabel')  # e.g., "Happy"
        show_value = self.props.get('showValue', True)
        label_always = self.props.get('labelAlways', False)
        
        with ui.column() as container:
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
                
                def update_value_display(e):
                    value_label.text = f'Value: {e.value}'
                
                slider.on('update:model-value', update_value_display)
        
        self.apply_styling_and_events(container, renderer)
        return container


class FormComponent(BaseComponent):
    """Generic form component that can render any form structure."""
    
    def render(self, renderer: 'MondrUIRenderer') -> Any:
        title = self.props.get('title', '')
        fields = self.props.get('fields', [])
        actions = self.props.get('actions', [])
        layout = self.props.get('layout', 'vertical')
        
        with ui.card() as form_card:
            if title:
                ui.label(title).classes('text-xl font-bold mb-4')
            
            # Create form layout
            if layout == 'horizontal':
                field_container = ui.row()
            else:
                field_container = ui.column()
            
            with field_container:
                # Render form fields
                for field in fields:
                    self._render_form_field(field, renderer)
            
            # Render action buttons
            if actions:
                with ui.row().classes('w-full justify-end mt-4 gap-2'):
                    for action in actions:
                        action_spec = {
                            'component': 'Button',
                            'props': {
                                'label': action.get('label', ''),
                                'variant': action.get('variant', 'default'),
                                'events': {
                                    'click': action.get('action', '')
                                }
                            }
                        }
                        renderer.render_component(action_spec)
        
        self.apply_styling_and_events(form_card, renderer)
        return form_card
    
    def _render_form_field(self, field: Dict[str, Any], renderer: 'MondrUIRenderer') -> None:
        """Render a single form field with label."""
        label = field.get('label', '')
        required = field.get('required', False)
        field_id = field.get('id', '')
        field_type = field.get('type', 'text')
        
        # Render label
        label_text = f"{label}{'*' if required else ''}"
        ui.label(label_text).classes('text-sm font-medium mb-1')
        
        # Render field based on type
        if field_type == 'radio':
            input_spec = {
                'component': 'Radio',
                'props': {
                    'options': field.get('options', {}),
                    'value': field.get('value'),
                    'inline': field.get('inline', False),
                    'style': {'classes': ['w-full', 'mb-3']}
                }
            }
        elif field_type == 'checkboxGroup':
            input_spec = {
                'component': 'CheckboxGroup',
                'props': {
                    'options': field.get('options', {}),
                    'value': field.get('value', []),
                    'layout': field.get('layout', 'vertical'),
                    'style': {'classes': ['w-full', 'mb-3']}
                }
            }
        elif field_type == 'slider':
            input_spec = {
                'component': 'Slider',
                'props': {
                    'min': field.get('min', 0),
                    'max': field.get('max', 100),
                    'step': field.get('step', 1),
                    'value': field.get('value', field.get('min', 0)),
                    'minLabel': field.get('minLabel'),
                    'maxLabel': field.get('maxLabel'),
                    'showValue': field.get('showValue', True),
                    'labelAlways': field.get('labelAlways', False),
                    'style': {'classes': ['w-full', 'mb-3']}
                }
            }
        else:
            # Default to Input component for standard input types
            input_spec = {
                'component': 'Input',
                'props': {
                    'inputType': field_type,
                    'placeholder': field.get('placeholder', ''),
                    'required': required,
                    'options': field.get('options', []),
                    'style': {'classes': ['w-full', 'mb-3']}
                }
            }
        
        if field_id:
            input_spec['props']['id'] = field_id
        
        renderer.render_component(input_spec)


class CardComponent(BaseComponent):
    """Generic card component."""
    
    def render(self, renderer: 'MondrUIRenderer') -> Any:
        title = self.props.get('title')
        
        card = ui.card()
        
        with card:
            if title:
                ui.label(title).classes('text-lg font-bold mb-2')
            
            # Render children
            for child_spec in self.children:
                renderer.render_component(child_spec)
        
        self.apply_styling_and_events(card, renderer)
        return card


class ListComponent(BaseComponent):
    """Generic list component."""
    
    def render(self, renderer: 'MondrUIRenderer') -> Any:
        items = self.props.get('items', [])
        item_template = self.props.get('itemTemplate', {})
        empty_message = self.props.get('emptyMessage', 'No items')
        
        with ui.column() as list_container:
            if not items:
                ui.label(empty_message).classes('text-gray-500 italic')
            else:
                for item in items:
                    if item_template:
                        # Merge item data with template
                        item_spec = self._merge_item_with_template(item, item_template)
                        renderer.render_component(item_spec)
                    else:
                        # Default to simple text representation
                        ui.label(str(item))
        
        self.apply_styling_and_events(list_container, renderer)
        return list_container
    
    def _merge_item_with_template(self, item: Any, template: Dict[str, Any]) -> Dict[str, Any]:
        """Merge item data with template specification."""
        # Simple template variable replacement
        spec = json.loads(json.dumps(template))  # Deep copy
        
        def replace_variables(obj):
            if isinstance(obj, str) and obj.startswith('{{') and obj.endswith('}}'):
                var_name = obj[2:-2].strip()
                return item.get(var_name, obj) if isinstance(item, dict) else str(item)
            elif isinstance(obj, dict):
                return {k: replace_variables(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_variables(v) for v in obj]
            return obj
        
        result = replace_variables(spec)
        # Ensure we return a dictionary
        if not isinstance(result, dict):
            return {'component': 'Text', 'props': {'text': str(result)}}
        return result


class MondrUIRenderer:
    """Generic, extensible UI renderer."""
    
    def __init__(self):
        """Initialize with standard component registry."""
        self.component_registry: Dict[str, Type[BaseComponent]] = {
            'Container': ContainerComponent,
            'Text': TextComponent,
            'Input': InputComponent,
            'Button': ButtonComponent,
            'Radio': RadioComponent,
            'CheckboxGroup': CheckboxGroupComponent,
            'Slider': SliderComponent,
            'Form': FormComponent,
            'Card': CardComponent,
            'List': ListComponent,
        }
        
        # Register template components
        self.template_registry: Dict[str, Dict[str, Any]] = {}
        self._register_builtin_templates()
        
        self.action_handlers: Dict[str, Callable] = {}
        self.theme: Dict[str, Any] = self._default_theme()
    
    def _default_theme(self) -> Dict[str, Any]:
        """Default theme configuration."""
        return {
            'colors': {
                'primary': '#007bff',
                'secondary': '#6c757d',
                'success': '#28a745',
                'danger': '#dc3545',
                'warning': '#ffc107',
                'info': '#17a2b8'
            },
            'spacing': {
                'xs': '0.25rem',
                'sm': '0.5rem',
                'md': '1rem',
                'lg': '1.5rem',
                'xl': '2rem'
            },
            'typography': {
                'fontFamily': 'Inter, sans-serif',
                'fontSize': '14px',
                'lineHeight': '1.5'
            }
        }
    
    def _register_builtin_templates(self):
        """Register built-in component templates."""
        # Bug report form template
        self.template_registry['bugReportForm'] = {
            'component': 'Form',
            'props': {
                'title': '{{title}}',
                'fields': '{{fields}}',
                'actions': '{{actions}}',
                'style': {
                    'classes': ['max-w-md', 'mx-auto', 'p-6']
                }
            }
        }
        
        # Chat interface template
        self.template_registry['chatInterface'] = {
            'component': 'Container',
            'props': {
                'layout': 'vertical',
                'children': [
                    {
                        'component': 'Container',
                        'props': {
                            'layout': 'horizontal',
                            'children': '{{children}}'
                        }
                    }
                ]
            }
        }
    
    def register_component(self, name: str, component_class: Type[BaseComponent]):
        """Register a new component type."""
        if not issubclass(component_class, BaseComponent):
            raise ValueError("Component must inherit from BaseComponent")
        self.component_registry[name] = component_class
    
    def register_template(self, name: str, template_spec: Dict[str, Any]):
        """Register a new template."""
        self.template_registry[name] = template_spec
    
    def register_action_handler(self, action: str, handler: Callable):
        """Register an action handler."""
        self.action_handlers[action] = handler
    
    def set_theme(self, theme: Dict[str, Any]):
        """Set custom theme."""
        self.theme.update(theme)
    
    def render_ui(self, spec: Dict[str, Any]) -> Any:
        """Render a UI component tree from specification."""
        if spec.get('type') != 'ui.render':
            raise ValueError("Specification must have type 'ui.render'")
        
        return self.render_component(spec)
    
    def render_component(self, spec: Dict[str, Any]) -> Any:
        """Render a single component from specification."""
        component_name = spec.get('component')
        if not component_name:
            raise ValueError("Component specification must include component name")
        
        props = spec.get('props', {})
        
        # Check if this is a template
        if component_name in self.template_registry:
            template_spec = self._expand_template(component_name, props)
            return self.render_component(template_spec)
        
        # Get component class
        component_class = self.component_registry.get(component_name)
        if not component_class:
            raise ValueError(f"Unknown component: {component_name}")
        
        # Create and render component
        component = component_class(component_name, props)
        
        if not component.validate_props():
            raise ValueError(f"Invalid properties for component: {component_name}")
        
        return component.render(self)
    
    def _expand_template(self, template_name: str, props: Dict[str, Any]) -> Dict[str, Any]:
        """Expand a template with provided properties."""
        template = self.template_registry[template_name]
        
        # Simple variable replacement
        def replace_variables(obj):
            if isinstance(obj, str) and obj.startswith('{{') and obj.endswith('}}'):
                var_name = obj[2:-2].strip()
                return props.get(var_name, obj)
            elif isinstance(obj, dict):
                return {k: replace_variables(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_variables(v) for v in obj]
            return obj
        
        result = replace_variables(template)
        # Ensure we return a dictionary
        if not isinstance(result, dict):
            raise ValueError(f"Template {template_name} must expand to a dictionary")
        return result


# Global renderer instance
_renderer = MondrUIRenderer()


def render_ui(spec: Dict[str, Any]) -> Any:
    """Render a UI component tree from a MondrUI specification."""
    return _renderer.render_ui(spec)


def register_component(name: str, component_class: Type[BaseComponent]):
    """Register a new component type globally."""
    _renderer.register_component(name, component_class)


def register_template(name: str, template_spec: Dict[str, Any]):
    """Register a new template globally."""
    _renderer.register_template(name, template_spec)


def register_action_handler(action: str, handler: Callable):
    """Register a global action handler."""
    _renderer.register_action_handler(action, handler)


def set_theme(theme: Dict[str, Any]):
    """Set global theme."""
    _renderer.set_theme(theme)


def parse_and_render(json_str: str) -> Any:
    """Parse JSON string and render UI component."""
    try:
        spec = json.loads(json_str)
        return render_ui(spec)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")


# Utility function to create custom components easily
def create_component(render_func: Callable) -> Type[BaseComponent]:
    """Create a component class from a render function."""
    
    class CustomComponent(BaseComponent):
        def render(self, renderer: MondrUIRenderer) -> Any:
            element = render_func(self.props, renderer)
            self.apply_styling_and_events(element, renderer)
            return element
    
    return CustomComponent
