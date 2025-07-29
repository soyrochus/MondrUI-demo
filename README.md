# MondrUI: A Specification for Conversational UI


| ![MondrUI](images/mondrui.png) | MondrUI is a test implementation and demo of conversational UI that enables dynamic user interface generation from JSON specifications. This project demonstrates how AI agents can create rich, interactive forms and interfaces on-demand during conversations, bridging the gap between natural language interaction and structured data collection. |
| :---- | :---- |



For detailed information about the MondrUI specification and concept, see: [MondrUI: A Specification for Conversational UI](mondrui_article.md)

## Features

- **Generic UI Rendering**: Create dynamic interfaces from JSON specifications
- **AI Integration**: Seamless integration with LangChain-based AI agents
- **Component System**: Extensible plugin architecture for custom components
- **Template Engine**: Reusable UI templates with variable substitution
- **Real-time Chat**: Modern AI chat with conversational memory
- **Type Safety**: Full type annotations and comprehensive testing

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. Make sure you have `uv` installed:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Clone the repository and install dependencies:

```bash
git clone https://github.com/soyrochus/MondrUI-demo.git
cd MondrUI-demo
uv sync
```

### Environment Setup

Create a `.env` file with your OpenAI API key:

```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

## Usage

### Running the Applications

The project includes several demo applications:

#### 1. Main Chat Application
```bash
uv run python main.py
```
Access at: http://localhost:8080

#### 2. MondrUI Component Demo
```bash
uv run python render_ui.py
```
Access at: http://localhost:8080

#### 3. AI + MondrUI Integration Demo
```bash
uv run python integration_demo.py
```
Access at: http://localhost:8081

### Running Tests

Run the comprehensive test suite:

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest test_mondrui.py -v

# Run with coverage
uv run pytest --cov=mondrui --cov-report=html
```

### Development

For development work:

```bash
# Install development dependencies
uv sync --dev

# Run linting
uv run ruff check .

# Run type checking
uv run mypy .

# Format code
uv run ruff format .
```

## Project Structure

```
MondrUI-demo/
├── ai.py                    # AI agent with modern LangChain memory
├── mondrui.py              # Core MondrUI rendering engine
├── main.py                 # Main chat application
├── render_ui.py            # Component showcase demo
├── integration_demo.py     # AI + MondrUI integration demo
├── test_mondrui.py         # Comprehensive test suite
├── log_callback_handler.py # Logging utilities
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
├── .env                    # Environment variables (create manually)
└── README.md               # This file
```

## MondrUI Specification

MondrUI uses JSON specifications to define UI components:

```json
{
  "type": "ui.render",
  "component": "bugReportForm",
  "props": {
    "title": "Report a Bug",
    "fields": [
      {"id": "summary", "label": "Summary", "type": "text", "required": true}
    ],
    "actions": [
      {"label": "Submit", "action": "submit_bug"}
    ]
  }
}
```

### Built-in Components

- **Container**: Layout components with horizontal/vertical arrangements
- **Text**: Text display with variants (h1, h2, p, etc.)
- **Input**: Form inputs (text, textarea, select, etc.)
- **Button**: Interactive buttons with variants and actions
- **Form**: Structured forms with validation
- **Card**: Content containers with titles
- **List**: Data display components

### Custom Components

Create and register custom components:

```python
from mondrui import register_component, create_component

def my_component_render(props, renderer):
    # Your custom rendering logic
    return ui_element

CustomComponent = create_component(my_component_render)
register_component('MyCustom', CustomComponent)
```

## API Documentation

### Core Functions

- `render_ui(spec)`: Render a UI from JSON specification
- `register_component(name, component_class)`: Register a new component type
- `register_template(name, template)`: Register a reusable template
- `create_component(render_func)`: Create a component from a render function

### AI Integration

```python
from ai import AIAgent

agent = AIAgent()
response = await agent.send_message("Hello!")
history = agent.get_conversation_history()
stats = agent.get_memory_stats()
```

## Examples

See the demo applications for comprehensive examples:

- **Basic Usage**: `render_ui.py` - Component showcase
- **AI Integration**: `integration_demo.py` - Chat with dynamic UI generation
- **Real Application**: `main.py` - Complete chat application

## Testing

The project includes 23+ comprehensive tests covering:

- Component rendering and validation
- Template system functionality
- Error handling and edge cases
- Custom component registration
- AI integration features

All tests pass and provide excellent coverage of the MondrUI system.



## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Copyright and license

Copyright © 2025 Iwan van der Kleijn

Licensed under the MIT License
[MIT](https://choosealicense.com/licenses/mit/)