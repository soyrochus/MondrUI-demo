#!/usr/bin/env python3
"""
Test the AI system with the updated prompt that includes new components.
"""

from ai import AIAgent
import asyncio

async def test_ai_with_new_components():
    """Test the AI agent with the survey form prompt."""
    
    ai_agent = AIAgent(model='gpt-4o-mini')
    
    prompt = """Create a user preference survey form with the following requirements:

1. A radio button group for selecting experience level (Beginner, Intermediate, Advanced)
2. A checkbox group for selecting preferred programming languages (Python, JavaScript, TypeScript, Go, Rust)  
3. A slider for rating overall satisfaction from 1-10 with labels "Very Dissatisfied" to "Very Satisfied"
4. A text input for additional comments
5. A submit button

Please generate the MondrUI JSON specification for this form."""
    
    print("Testing AI with updated system prompt...")
    print("=" * 60)
    print(f"Prompt: {prompt}")
    print("=" * 60)
    print("AI Response:")
    print()
    
    response = ""
    async for chunk in ai_agent.send_message(prompt):
        response += chunk
        print(chunk, end="", flush=True)
    
    print("\n" + "=" * 60)
    print("Response completed!")
    
    # Check if the response contains the new component types
    if '"type": "radio"' in response:
        print("✅ Radio component detected in response")
    else:
        print("❌ Radio component NOT found in response")
        
    if '"type": "checkboxGroup"' in response:
        print("✅ CheckboxGroup component detected in response")
    else:
        print("❌ CheckboxGroup component NOT found in response")
        
    if '"type": "slider"' in response:
        print("✅ Slider component detected in response")
    else:
        print("❌ Slider component NOT found in response")
    
    return response

if __name__ == "__main__":
    asyncio.run(test_ai_with_new_components())
