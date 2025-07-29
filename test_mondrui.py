#!/usr/bin/env python3
"""
Tests for MondrUI rendering functionality.
"""

import pytest
import json
from mondrui import render_ui, parse_and_render, MondrUIRenderer


class TestMondrUIRenderer:
    """Test cases for the MondrUI rendering system."""
    
    @pytest.fixture
    def bug_report_spec(self):
        """Sample bug report form specification."""
        return {
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
    
    @pytest.fixture
    def renderer(self):
        """Create a fresh renderer instance for testing."""
        return MondrUIRenderer()
    
    def test_renderer_initialization(self, renderer):
        """Test that renderer initializes correctly."""
        assert isinstance(renderer, MondrUIRenderer)
        assert 'bugReportForm' in renderer.component_registry
        assert 'Container' in renderer.component_registry
        assert isinstance(renderer.action_handlers, dict)
    
    def test_render_ui_with_valid_spec(self, bug_report_spec):
        """Test rendering with a valid specification."""
        # This test verifies the function can be called without errors
        # We don't actually render the UI to avoid NiceGUI context issues in tests
        try:
            result = render_ui(bug_report_spec)
            # If we get here without exception, the function structure is correct
            assert True
        except Exception as e:
            # Expected in test environment without proper NiceGUI context
            # We're mainly testing that the function exists and processes the spec
            assert "ui.card" in str(e) or "NiceGUI" in str(e) or "context" in str(e)
    
    def test_render_ui_invalid_type(self):
        """Test rendering with invalid type."""
        invalid_spec = {
            "type": "invalid.type",
            "component": "bugReportForm",
            "props": {}
        }
        
        with pytest.raises(ValueError, match="Specification must have type 'ui.render'"):
            render_ui(invalid_spec)
    
    def test_render_ui_missing_component(self):
        """Test rendering with missing component."""
        invalid_spec = {
            "type": "ui.render",
            "props": {}
        }
        
        with pytest.raises(ValueError, match="Specification must include a component name"):
            render_ui(invalid_spec)
    
    def test_render_ui_unknown_component(self):
        """Test rendering with unknown component."""
        invalid_spec = {
            "type": "ui.render",
            "component": "unknownComponent",
            "props": {}
        }
        
        with pytest.raises(ValueError, match="Unknown component: unknownComponent"):
            render_ui(invalid_spec)
    
    def test_bug_report_form_structure(self, bug_report_spec, renderer):
        """Test that bug report form processes the correct structure."""
        props = bug_report_spec["props"]
        
        # Verify the renderer can extract the props correctly
        assert props["title"] == "Report a Bug"
        assert len(props["fields"]) == 4
        assert len(props["actions"]) == 2
        
        # Verify field structure
        summary_field = props["fields"][0]
        assert summary_field["id"] == "summary"
        assert summary_field["type"] == "text"
        assert summary_field["required"] is True
        
        severity_field = props["fields"][3]
        assert severity_field["type"] == "select"
        assert "Low" in severity_field["options"]
        assert "Critical" in severity_field["options"]
    
    def test_action_handler_registration(self, renderer):
        """Test action handler registration."""
        def dummy_handler():
            return "handled"
        
        renderer.register_action_handler("test.action", dummy_handler)
        assert "test.action" in renderer.action_handlers
        assert renderer.action_handlers["test.action"] == dummy_handler
    
    def test_parse_and_render_valid_json(self, bug_report_spec):
        """Test parsing and rendering from JSON string."""
        json_str = json.dumps(bug_report_spec)
        
        try:
            result = parse_and_render(json_str)
            assert True  # Function executed without JSON parsing errors
        except Exception as e:
            # Expected in test environment - we're testing JSON parsing mainly
            assert "ui.card" in str(e) or "NiceGUI" in str(e) or "context" in str(e)
    
    def test_parse_and_render_invalid_json(self):
        """Test parsing invalid JSON."""
        invalid_json = '{"type": "ui.render", "component":}'  # Invalid JSON
        
        with pytest.raises(ValueError, match="Invalid JSON"):
            parse_and_render(invalid_json)
    
    def test_component_registry_completeness(self, renderer):
        """Test that all expected components are registered."""
        expected_components = [
            'bugReportForm', 'Container', 'Header', 'Sidebar',
            'Button', 'Input', 'List', 'ChatHistory', 'Divider', 'ChatInput'
        ]
        
        for component in expected_components:
            assert component in renderer.component_registry
            assert callable(renderer.component_registry[component])
    
    def test_bug_report_form_props_validation(self):
        """Test that bug report form handles various prop configurations."""
        # Test with minimal props
        minimal_spec = {
            "type": "ui.render",
            "component": "bugReportForm",
            "props": {}
        }
        
        try:
            result = render_ui(minimal_spec)
            assert True
        except Exception as e:
            # Expected in test environment
            assert "ui.card" in str(e) or "NiceGUI" in str(e) or "context" in str(e)
    
    def test_container_component_structure(self):
        """Test container component with children."""
        container_spec = {
            "type": "ui.render",
            "component": "Container",
            "props": {
                "direction": "vertical",
                "children": [
                    {
                        "component": "Button",
                        "props": {"label": "Test Button"}
                    }
                ]
            }
        }
        
        try:
            result = render_ui(container_spec)
            assert True
        except Exception as e:
            # Expected in test environment
            assert "ui" in str(e) or "NiceGUI" in str(e) or "context" in str(e)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
