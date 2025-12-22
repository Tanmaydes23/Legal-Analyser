"""Simple test of the full analysis pipeline"""
import sys
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv()

from ai_analyzer import LegalAIAnalyzer
from clause_extractor import ClauseExtractor  
from risk_analyzer import RiskAnalyzer

# Test document
test_doc = """
RENTAL AGREEMENT

This agreement is made between John Smith (Landlord) and Jane Doe (Tenant).

1. Payment Terms
The tenant shall pay $2000 per month, due on the 1st of each month.

2. Termination
Either party may terminate this agreement with 30 days written notice.
"""

print("Testing full analysis pipeline...\n")

try:
    # Test AI Analyzer
    print("1. Testing AI Analyzer...")
    ai_analyzer = LegalAIAnalyzer()
    ai_result = ai_analyzer.analyze_complete(test_doc)
    print(f"   ✅ AI Analysis: {ai_result['summary']['summary'][:100]}...")
    
    # Test Clause Extractor
    print("\n2. Testing Clause Extractor...")
    clause_extractor = ClauseExtractor()
    clauses = clause_extractor.extract_clauses(test_doc)
    print(f"   ✅ Found {len(clauses)} clauses")
    
    # Test Risk Analyzer
    print("\n3. Testing Risk Analyzer...")
    risk_analyzer = RiskAnalyzer()
    risk_result = risk_analyzer.analyze_document_risk(test_doc, clauses)
    print(f"   ✅ Risk Score: {risk_result['overall_risk_score']}/100")
    
    print("\n✅ ALL TESTS PASSED!")
    print("The backend should work correctly now.")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    print("\nFull traceback:")
    print(traceback.format_exc())
