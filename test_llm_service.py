"""
Test script for the refactored LLM Service
Tests OpenAI structured output, Claude text generation, and Llama image-to-text capabilities
"""

import os
import base64
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

# Import our refactored LLM service
from llm_service import (
    LLMService, 
    LLMRequest, 
    StructuredLLMRequest, 
    ModelConfig, 
    ProviderType
)

# Import the extensions
from llm_service_extension import extend_llm_service, ImageToTextRequest

# Apply the extensions to the module
import llm_service
extend_llm_service(llm_service)

# Load environment variables from .env file
load_dotenv()

# Simple boolean response model for structured output
class BooleanResponse(BaseModel):
    is_true: bool
    confidence: Optional[float] = None
    reasoning: Optional[str] = None

def read_image_as_base64(image_path):
    """Read an image file and convert it to base64 encoding"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error reading image file: {e}")
        return None

def test_openai_structured():
    """Test OpenAI's o3-mini model with structured boolean output"""
    print("\n===== Testing OpenAI o3-mini with structured boolean output =====")
    
    llm_service = LLMService()
    
    # Create a request for a simple true/false classification
    request = StructuredLLMRequest(
        user_prompt="Is the following statement true or false? 'Python is a compiled programming language.'",
        system_prompt="You are a fact-checking AI. Determine if statements are true or false.",
        model_config=ModelConfig(
            provider=ProviderType.OPENAI,
            model_name="o3-mini"
        ),
        response_model=BooleanResponse,
        temperature=0.1  # Low temperature for more deterministic output
    )
    
    try:
        # Get the structured response
        response = llm_service.generate_structured(request)
        
        # Print the results
        print(f"Statement: 'Python is a compiled programming language.'")
        print(f"Response: {response.is_true}")
        print(f"Confidence: {response.confidence}")
        print(f"Reasoning: {response.reasoning}")
        
        return True
    except Exception as e:
        print(f"Error testing OpenAI structured output: {e}")
        return False

def test_claude_text():
    """Test Claude's text generation capabilities"""
    print("\n===== Testing Claude 3.7 Sonnet with text generation =====")
    
    llm_service = LLMService()
    
    # Create a request for text generation
    request = LLMRequest(
        user_prompt="Explain the difference between supervised and unsupervised learning in machine learning in under 200 words.",
        system_prompt="You are an AI teaching assistant specializing in machine learning concepts.",
        model_config=ModelConfig(
            provider=ProviderType.ANTHROPIC,
            model_name="claude-3-7-sonnet-20250219"
        ),
        temperature=0.7  # More creative temperature for text generation
    )
    
    try:
        # Get the text response
        response = llm_service.generate(request)
        
        # Print the result
        print("Query: Explain the difference between supervised and unsupervised learning")
        print(f"Response:\n{response}")
        
        return True
    except Exception as e:
        print(f"Error testing Claude text generation: {e}")
        return False

def test_llama_image():
    """Test Llama's image-to-text capabilities"""
    print("\n===== Testing Llama 3.2 Vision with image description =====")
    
    # Use the improved ImageToTextRequest
    image_path = "screenshot.png"
    
    # Create an instance of the extended LLMService
    llm_service = LLMService()
    
    # Create an image-to-text request
    request = ImageToTextRequest(
        user_prompt="",  # Not used directly with image request
        image_path=image_path,
        image_description_prompt="Describe what you see in this image in detail.",
        system_prompt="You are a helpful assistant that can see and describe images accurately.",
        model_config=ModelConfig(
            provider=ProviderType.GROQ,
            model_name="llama-3.2-90b-vision-preview"
        ),
        temperature=0.7,
        max_tokens=1024
    )
    
    try:
        # Use the new process_image method
        response = llm_service.process_image(request)
        
        # Print the result
        print(f"Image: {image_path}")
        print(f"Description:\n{response}")
        
        return True
    except Exception as e:
        print(f"Error testing Llama image description: {e}")
        return False

if __name__ == "__main__":
    print("Testing LLM Service with multiple providers")
    
    # Verify environment variables
    required_keys = {
        "OPENAI_API_KEY": "OpenAI",
        "ANTHROPIC_API_KEY": "Anthropic/Claude",
        "GROQ_API_KEY": "Groq/Llama"
    }
    
    for env_var, provider_name in required_keys.items():
        if not os.getenv(env_var):
            print(f"Warning: {env_var} not found in environment. {provider_name} tests will fail.")
    
    # Run the tests
    results = []
    
    # Test 1: OpenAI structured output
    results.append(("OpenAI structured", test_openai_structured()))
    
    # Test 2: Claude text generation
    results.append(("Claude text", test_claude_text()))
    
    # Test 3: Llama image description
    results.append(("Llama image", test_llama_image()))
    
    # Print summary
    print("\n===== Test Results =====")
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")