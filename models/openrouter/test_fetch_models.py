#!/usr/bin/env python3
"""
Test script for OpenRouter fetch-from-remote functionality
"""

import sys
import os
import json
from typing import Dict, Any

# Add the provider directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'provider'))

def test_fetch_models():
    """Test the fetch-from-remote functionality"""
    
    # Import the provider
    try:
        from openrouter import OpenRouterProvider
        from dify_plugin.entities.model import ModelType
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please make sure you have the required dependencies installed")
        return False
    
    # Initialize provider
    provider = OpenRouterProvider()
    
    # Test credentials (you need to provide a valid API key)
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("Please set OPENROUTER_API_KEY environment variable")
        print("Example: export OPENROUTER_API_KEY=your_api_key_here")
        return False
    
    credentials = {
        'api_key': api_key
    }
    
    print("Testing OpenRouter fetch-from-remote functionality...")
    print("=" * 50)
    
    try:
        # Test credential validation
        print("1. Testing credential validation...")
        provider.validate_provider_credentials(credentials)
        print("✅ Credential validation passed")
        
        # Test model fetching
        print("\n2. Testing model fetching...")
        models = provider.get_models(ModelType.LLM, credentials)
        
        if not models:
            print("❌ No models returned")
            return False
            
        print(f"✅ Successfully fetched {len(models)} models")
        
        # Display first few models as examples
        print("\n3. Sample models:")
        print("-" * 30)
        
        for i, model in enumerate(models[:5]):  # Show first 5 models
            print(f"Model {i+1}:")
            print(f"  ID: {model.model}")
            print(f"  Name: {model.label.get('en_US', 'N/A')}")
            print(f"  Features: {model.features}")
            print(f"  Context Size: {model.model_properties.get('context_size', 'N/A')}")
            print(f"  Pricing: Input=${model.pricing.get('input', 'N/A')}, Output=${model.pricing.get('output', 'N/A')}")
            print()
        
        if len(models) > 5:
            print(f"... and {len(models) - 5} more models")
        
        print("\n4. Testing specific model types:")
        print("-" * 30)
        
        # Count models by features
        vision_models = [m for m in models if 'vision' in m.features]
        tool_call_models = [m for m in models if 'tool-call' in m.features]
        
        print(f"  Vision-capable models: {len(vision_models)}")
        print(f"  Tool-calling models: {len(tool_call_models)}")
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_fetch_models()
    sys.exit(0 if success else 1)
