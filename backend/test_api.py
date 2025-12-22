"""
Simple test script - bypasses all complex analysis
"""
import sys
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv()

# Just test document upload and basic response
print("Testing basic API flow...")

import requests

# Test health check
response = requests.get("http://localhost:8000/")
print(f"Health check: {response.json()}")

# Create a simple text file
with open("test_doc.txt", "w") as f:
    f.write("This is a simple rental agreement for testing.")

# Test upload
with open("test_doc.txt", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/upload",
        files={"file": ("test.txt", f, "text/plain")}
    )
    print(f"Upload response: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        doc_id = data['document_id']
        print(f"Document ID: {doc_id}")
        
        # Try analysis
        print("\\nAttempting analysis...")
        response = requests.post(f"http://localhost:8000/api/analyze/{doc_id}")
        print(f"Analysis status: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
        else:
            print("SUCCESS!")
