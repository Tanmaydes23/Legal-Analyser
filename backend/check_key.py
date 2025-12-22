import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Check for Groq API key
groq_key = os.getenv('GROQ_API_KEY')

if groq_key:
    print(f"✅ GROQ_API_KEY is SET")
    print(f"   Key starts with: {groq_key[:20]}...")
    print(f"   Key length: {len(groq_key)} characters")
else:
    print("❌ GROQ_API_KEY is NOT SET")
    print("   Please add it to your .env file:")
    print("   GROQ_API_KEY=gsk_your_key_here")
