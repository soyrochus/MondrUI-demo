# MondrUI: A Specification for Conversational UI

## Letting the AI Drive the Interface

## Introduction

The term *Conversational UI* is often misunderstood. For many, it simply evokes a chatbot that exchanges text with users. But a truly conversational UI goes far beyond basic dialogue. It involves an interface whose **structure and behavior are determined dynamically by the AI**—in real time, and in response to user intent and context. This creates a fluid and adaptive experience, where the boundary between “conversation” and “interface” dissolves.

| ![MondrUI](images/mondrui.png) | In this article we want to present MondrUI as an implementation of this compositional UI—bridging the gap between intent and interface, and letting the conversation itself shape the experience. |
| :---- | :---- |

## Not Just Chatbots, Not Just Forms

Let’s be clear: conversational UI is **not** about generating raw HTML or JavaScript, nor is it about cobbling together rigid, pre-programmed components. Instead, it is about defining a **contract** between the AI and the rendering layer. This contract is typically implemented as a **Domain-Specific Language (DSL)** or high-level API. The AI uses the DSL to describe *what* should be rendered; the UI layer takes care of *how* to render it.

### **Why is This a Paradigm Shift?**

Traditional UI systems are static, menu-driven, or rely on developer-specified flows. In contrast, MondrUI allows the AI to *assemble* the UI from composable parts—widgets, forms, lists, layouts—at runtime, based on conversational context and user intent. This allows for seamless transitions between unstructured conversation and structured workflows, such as reporting a bug, uploading a document, or exploring data, all without the need for pre-programmed screens.

## A Layered Architecture

This approach enforces clear architectural separation:

* **AI Agent:** Interprets user intent and translates it into structured instructions.

* **DSL Interface:** Provides a limited, controlled vocabulary for the AI to express UI decisions in a declarative way.

* **UI Rendering Engine:** Receives these instructions and renders the interactive interface accordingly, using a registry of reusable components.

## By enforcing this separation, we gain **flexibility, safety, and reusability**. The AI never writes imperative code. It simply emits structured, declarative specifications, while the rendering engine ensures consistency and compliance with organizational standards.

## Ensuring Consistency: Templates and Rules

While this model allows great flexibility, real-world applications require a consistent user experience. MondrUI achieves this in two ways:

### **Templates in the DSL**

Templates are named blueprints—predefined sets of fields, layouts, and styling—that guarantee repeatability. For example, a `bugReportForm` template always includes a summary field, description, steps to reproduce, and severity selector, with consistent ordering and style. When the AI wants to present this form, it simply refers to the template, ensuring the UI always looks and behaves the same way for that function.

For example, the following json:

{  
  "type": "ui.render",  
  "component": "bugReportForm",  
  "props": {  
    "title": "Report a Bug",  
    "fields": \[  
      { "id":"summary", "label":"Bug Summary", "type":"text", "required":true },  
      { "id":"description", "label":"Description", "type":"textarea", "required":true },  
      { "id":"steps", "label":"Steps to Reproduce", "type":"textarea", "required":false },  
      { "id":"severity", "label":"Severity", "type":"select", "options":\["Low","Medium","High","Critical"\], "required":true }  
    \],  
    "actions": \[  
      { "id":"submit", "label":"Submit", "type":"submit", "target":"bug.report" },  
      { "id":"cancel", "label":"Cancel", "type":"cancel", "target":"chat.resume" }  
    \]  
  }  
}

Would result in the display of this form: 

![][image2]

### **Rules and Restrictions**

Beyond templates, *rules* ensure the AI’s instructions always conform to business requirements and brand guidelines. Examples include:

*  **Field order:** Enforce a specific sequence of inputs (e.g., summary before description).

* **Validation constraints:** Make fields required, or restrict allowed values (e.g., “severity” must be one of four values).

*  **Theming and styling:** Ensure every form, button, or dialog fits the organization’s visual identity.

## These rules are enforced by the rendering engine, ensuring even dynamically constructed forms remain consistent and compliant.

## Contextual Assembly: From Intent to UI

MondrUI does not simply define static screens. Instead, it enables the dynamic *assembly* of visual interfaces by the AI, drawing from a registry of composable widgets (buttons, lists, containers, forms, etc.). The AI, guided by user intent and system state, decides which components to instantiate, with what data and configuration, and how to connect them into a coherent interface.

**For example:** If the user says, "I'd like to report a bug," the AI can instantly emit a DSL instruction invoking the `bugReportForm` template. The rendering engine overlays the modal bug report form directly atop the ongoing chat. After submission or cancellation, the conversation resumes, context preserved.

## Beyond the Example: Compositional Power

A key advantage of MondrUI’s approach is **compositionality**. Developers (or even the AI) can describe full applications—such as a ChatGPT-style interface, analytics dashboard, or support workflow—entirely in the DSL. Each interface is a tree of containers and widgets, assembled to suit the user’s journey in real time.

This also enables **multi-modal UIs**: conversational threads, sidebar navigation, action menus, search inputs, and dynamically updating lists—all specified as declarative components, all coordinated by AI-driven logic.

## Implications and Benefits

This pattern enables a truly **adaptive, intent-driven user experience**:

*  **Modularity:** UIs are composed from reusable primitives, but always consistently.

*  **Adaptivity:** The interface evolves based on user interaction and system state, not pre-defined menus.

* **Seamless UX:** Forms and workflows emerge organically from conversation.

* **Decoupled Logic:** AI and UI can evolve independently—each can be improved without risk to the other.

* **Governance:** Templates and rules enable compliance, auditability, and design consistency.

Conversational UI is not just about making chatbots smarter—it’s about merging the flexibility of natural language with the precision of structured interfaces, without sacrificing control or consistency. The result is a more intelligent, user-centric interaction paradigm.

## Appendix: Complete MondrUI Schema Example

Below is a full **MondrUI DSL example** describing a ChatGPT-like conversational UI, including a sidebar with new chat button, search input, and a conversation list, alongside the main chat area.

## For example, the following json:



{  
  "type": "ui.render",  
  "component": "Container",  
  "props": {  
    "direction": "vertical",  
    "children": \[  
      {  
        "component": "Header",  
        "props": {  
          "title": "MondrUI Chat",  
          "actions": \[  
            { "icon": "settings", "action": "openSettings" }  
          \]  
        }  
      },  
      {  
        "component": "Container",  
        "props": {  
          "direction": "horizontal",  
          "children": \[  
            {  
              "component": "Sidebar",  
              "props": {  
                "direction": "vertical",  
                "width": "240px",  
                "children": \[  
                  {  
                    "component": "Button",  
                    "props": {  
                      "label": "New Chat",  
                      "icon": "plus",  
                      "onClick": "startNewChat"  
                    }  
                  },  
                  {  
                    "component": "Input",  
                    "props": {  
                      "placeholder": "Search chat...",  
                      "onChange": "searchConversations"  
                    }  
                  },  
                  {  
                    "component": "List",  
                    "props": {  
                      "data": "@get\_conversation\_list",  
                      "itemComponent": "ConversationListItem",  
                      "emptyMessage": "No conversations found"  
                    }  
                  }  
                \]  
              }  
            },  
            {  
              "component": "Container",  
              "props": {  
                "direction": "vertical",  
                "grow": true,  
                "children": \[  
                  {  
                    "component": "ChatHistory",  
                    "props": {  
                      "messages": "{{messages}}"  
                    }  
                  },  
                  {  
                    "component": "Divider",  
                    "props": { "margin": "md" }  
                  },  
                  {  
                    "component": "ChatInput",  
                    "props": {  
                      "onSend": "sendMessage",  
                      "placeholder": "Type your message..."  
                    }  
                  }  
                \]  
              }  
            }  
          \]  
        }  
      }  
    \]  
  }  
}



Would result in the display of this window:



## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Copyright and license

Copyright © 2025 Iwan van der Kleijn

Licensed under the MIT License
[MIT](https://choosealicense.com/licenses/mit/)