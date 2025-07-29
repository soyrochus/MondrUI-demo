#!/usr/bin/env python3
"""
Test script for the new interactive components: Radio, CheckboxGroup, and Slider
"""

from mondrui import render_ui
import json

def test_radio_component():
    """Test Radio component rendering."""
    spec = {
        "type": "ui.render",
        "component": "Radio",
        "props": {
            "id": "priority",
            "options": {"low": "Low Priority", "medium": "Medium Priority", "high": "High Priority"},
            "value": "medium",
            "inline": True
        }
    }
    
    try:
        result = render_ui(spec)
        print("✅ Radio component test passed")
        return True
    except Exception as e:
        print(f"❌ Radio component test failed: {e}")
        return False

def test_checkbox_group_component():
    """Test CheckboxGroup component rendering."""
    spec = {
        "type": "ui.render",
        "component": "CheckboxGroup",
        "props": {
            "id": "features",
            "options": {
                "notifications": "Email Notifications",
                "darkmode": "Dark Mode",
                "analytics": "Usage Analytics"
            },
            "value": ["notifications", "darkmode"],
            "layout": "vertical"
        }
    }
    
    try:
        result = render_ui(spec)
        print("✅ CheckboxGroup component test passed")
        return True
    except Exception as e:
        print(f"❌ CheckboxGroup component test failed: {e}")
        return False

def test_slider_component():
    """Test Slider component rendering."""
    spec = {
        "type": "ui.render",
        "component": "Slider",
        "props": {
            "id": "satisfaction",
            "min": 1,
            "max": 10,
            "step": 1,
            "value": 7,
            "minLabel": "Very Dissatisfied",
            "maxLabel": "Very Satisfied",
            "showValue": True,
            "labelAlways": True
        }
    }
    
    try:
        result = render_ui(spec)
        print("✅ Slider component test passed")
        return True
    except Exception as e:
        print(f"❌ Slider component test failed: {e}")
        return False

def test_enhanced_form():
    """Test Form component with new field types."""
    spec = {
        "type": "ui.render",
        "component": "Form",
        "props": {
            "title": "User Preferences Survey",
            "fields": [
                {
                    "id": "priority",
                    "label": "Priority Level",
                    "type": "radio",
                    "options": {"low": "Low", "medium": "Medium", "high": "High"},
                    "value": "medium",
                    "inline": True
                },
                {
                    "id": "features",
                    "label": "Desired Features",
                    "type": "checkboxGroup",
                    "options": {
                        "notifications": "Email Notifications",
                        "darkmode": "Dark Mode",
                        "analytics": "Usage Analytics"
                    },
                    "value": ["notifications"],
                    "layout": "vertical"
                },
                {
                    "id": "satisfaction",
                    "label": "Overall Satisfaction",
                    "type": "slider",
                    "min": 1,
                    "max": 10,
                    "minLabel": "Very Dissatisfied",
                    "maxLabel": "Very Satisfied",
                    "value": 7,
                    "showValue": True
                }
            ],
            "actions": [
                {"label": "Submit Survey", "action": "submit_survey", "variant": "primary"}
            ]
        }
    }
    
    try:
        result = render_ui(spec)
        print("✅ Enhanced Form component test passed")
        return True
    except Exception as e:
        print(f"❌ Enhanced Form component test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing new MondrUI interactive components...")
    print("=" * 50)
    
    tests = [
        test_radio_component,
        test_checkbox_group_component,
        test_slider_component,
        test_enhanced_form
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The new components are working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
