"""Test Groq API connection"""
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Get API key
api_key = os.getenv('GROQ_API_KEY')
print(f"API Key loaded: {'YES' if api_key else 'NO'}")
if api_key:
    print(f"Key starts with: {api_key[:10]}...")

# Try to initialize Groq client
try:
    client = Groq(api_key=api_key)
    print("✅ Groq client initialized successfully")
    
    # Try a simple API call
    print("\nTesting API call...")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Dec 2024 model
        messages=[
            {"role": "user", "content": "Say 'Hello' in one word"}
        ],
        max_tokens=10
    )
    
    print(f"✅ API call successful!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    print(f"\nFull traceback:")
    print(traceback.format_exc())
