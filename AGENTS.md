# AI Agent Instructions for MondrUI Enhancement

This document provides instructions for AI agents working on the MondrUI demo project to enhance the chat interface with dynamic form rendering capabilities.

## 1. Understanding NiceGUI Framework

For comprehensive information about NiceGUI and its capabilities, refer to:
- **Primary Documentation**: `.github/instructions.md` (contains detailed NiceGUI usage patterns and best practices)
- **Official Documentation**: [NiceGUI Documentation](https://nicegui.io/)

NiceGUI is a Python web framework that allows you to create interactive web applications using familiar Python syntax. Key concepts:
- UI elements are created using `ui.element()` calls
- Elements can be nested using context managers (`with ui.element():`)
- Event handling is done through callbacks
- Real-time updates are supported for dynamic interfaces

## 2. Project Structure

For detailed project structure and setup instructions, see the main [README.md](README.md).

### Key Files for This Task:
```
MondrUI-demo/
├── main.py                 # 🎯 TARGET - Basic chat interface to extend
├── ai.py                   # AI agent with LangChain memory system  
├── mondrui.py              # Core MondrUI rendering engine
├── integration_demo.py     # Reference implementation for AI+MondrUI
├── render_ui.py            # MondrUI component showcase
└── test_mondrui.py         # Test suite for validation
```

### Current Architecture:
- **main.py**: Contains basic chat interface with memory display
- **ai.py**: Modern AI agent with conversation memory using LangChain 0.3+
- **mondrui.py**: Generic UI rendering system that processes JSON specifications
- **MondrUI JSON Format**: Specifications follow this pattern:
  ```json
  {
    "type": "ui.render",
    "component": "bugReportForm",
    "props": {
      "title": "Form Title",
      "fields": [...],
      "actions": [...]
    }
  }
  ```

## 3. Required Changes

### Objective
Extend the basic chat interface in `main.py` so that the AI can:
1. Determine when to send a MondrUI JSON specification
2. Render the JSON as an interactive form (in a model form "on top of". the screen)
3. Collect user input from the form
4. Pass the form data back to the AI
5. Have the AI report on the received input

### Implementation Requirements

#### 3.1 AI Decision Logic
The AI should be able to determine when to render a form based on conversation context. Examples:
- User says "I want to report a bug" → Render bug report form
- User says "I need help with..." → Render help request form
- User asks for structured input → Render appropriate form

#### 3.2 Form Rendering Integration
Extend `main.py` to:
- Detect when AI response contains MondrUI JSON
- Parse and render the JSON using the existing `render_ui()` function
- Display the form within the chat interface
- Handle form submission and data collection

#### 3.3 Data Flow
```
User Message → AI → MondrUI JSON → Form Render → User Fills Form → Submit → Data to AI → AI Response
```

#### 3.4 Reference Implementation
Study `integration_demo.py` for examples of:
- Custom component creation
- MondrUI JSON specifications
- Form data handling
- AI integration patterns

### Technical Specifications

#### 3.4.1 JSON Detection
The AI should format MondrUI responses using a recognizable pattern:
```python
# Example AI response with embedded MondrUI
response = """I'll help you report that bug. Please fill out this form:

```json
{
  "type": "ui.render", 
  "component": "bugReportForm",
  "props": {
    "title": "Bug Report",
    "fields": [
      {"id": "summary", "label": "Bug Summary", "type": "text", "required": true},
      {"id": "description", "label": "Description", "type": "textarea", "required": true}
    ],
    "actions": [
      {"label": "Submit Bug Report", "action": "submit_bug"}
    ]
  }
}
```

Please fill out the form and click submit when ready."""
```

#### 3.4.2 Form Integration Points
Modify `main.py` to add:
1. **JSON Parser**: Extract MondrUI JSON from AI responses
2. **Form Container**: UI area for rendered forms
3. **Data Collector**: Capture form submission data
4. **Response Handler**: Send form data back to AI

#### 3.4.3 Error Handling
Implement robust error handling for:
- Invalid JSON in AI responses
- Unknown MondrUI components
- Form validation errors
- Network/AI response failures

### Expected Behavior

1. **Normal Chat**: Regular conversation continues as before
2. **Form Trigger**: When AI determines form is needed, it sends MondrUI JSON
3. **Form Render**: JSON is parsed and rendered as interactive form
4. **User Interaction**: User fills out and submits form
5. **Data Return**: Form data is sent back to AI with confirmation
6. **AI Acknowledgment**: AI reports on received data and continues conversation

### Testing Requirements

After implementation:
1. Test normal chat functionality remains unchanged
2. Test form rendering with various MondrUI components
3. Test form data collection and submission
4. Test error scenarios (invalid JSON, network issues)
5. Verify AI receives and can process form data

### Success Criteria

✅ AI can determine when forms are needed
✅ MondrUI JSON is correctly parsed from AI responses  
✅ Forms render properly within the chat interface
✅ Form data is collected and returned to AI
✅ AI acknowledges and reports on received form data
✅ Error handling works for edge cases
✅ Original chat functionality is preserved

### Notes for Implementation

- Use existing `render_ui()` function from `mondrui.py`
- Follow patterns established in `integration_demo.py`
- Maintain the existing AI memory system in `ai.py`
- Preserve the current UI layout and styling
- Ensure mobile-responsive design
- Add appropriate loading states and user feedback

This enhancement will demonstrate the full potential of conversational UI where AI agents can dynamically create structured data collection interfaces during natural language conversations.
