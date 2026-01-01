"""
Legal AI Analyzer using Groq API
Fast inference with Llama models
"""
from groq import Groq
import os
from typing import Dict, List

class LegalAIAnalyzer:
    """Legal document analysis using Groq"""
    
    def __init__(self):
        """Initialize Groq client"""
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"  # Current Groq model (Dec 2024)
    
    def _call_groq(self, prompt: str, max_tokens: int = 2000) -> str:
        """Call Groq API with prompt"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a legal document analysis expert. Provide clear, accurate analysis in a structured format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling Groq API: {str(e)}"
    
    def summarize_document(self, document_text: str) -> Dict:
        """Generate executive summary of legal document"""
        prompt = f"""Analyze this legal document and provide a comprehensive summary.

Document:
{document_text[:8000]}

Provide:
1. Document Type
2. Key Parties Involved
3. Main Purpose
4. Important Dates
5. Key Obligations
6. Primary Terms
7. Notable Clauses

Format as clear, structured text."""

        summary = self._call_groq(prompt, max_tokens=1500)
        
        return {
            'summary': summary,
            'document_type': self._extract_doc_type(summary),
        }
    
    def _extract_doc_type(self, summary: str) -> str:
        """Extract document type from summary"""
        summary_lower = summary.lower()
        doc_types = {
            'employment': ['employment', 'job', 'work agreement'],
            'rental': ['rental', 'lease', 'tenancy'],
            'service': ['service agreement', 'consulting'],
            'sales': ['purchase', 'sale', 'sales agreement'],
            'nda': ['non-disclosure', 'confidentiality', 'nda'],
            'partnership': ['partnership', 'joint venture'],
        }
        
        for doc_type, keywords in doc_types.items():
            if any(keyword in summary_lower for keyword in keywords):
                return doc_type.title()
        
        return 'General Contract'
    
    def extract_clauses(self, document_text: str) -> Dict:
        """Extract key clauses using AI"""
        prompt = f"""Extract and categorize the key clauses from this legal document.

Document:
{document_text[:8000]}

List each clause with:
- Type (e.g., Payment, Termination, Liability)
- Brief description
- Risk level (Low/Medium/High)

Format as a numbered list."""

        clauses_text = self._call_groq(prompt, max_tokens=2000)
        
        return {
            'clauses': clauses_text,
            'count': clauses_text.count('\n') if clauses_text else 0
        }
    
    def assess_risks(self, document_text: str) -> Dict:
        """AI-based risk assessment"""
        prompt = f"""Analyze the risks in this legal document.

Document:
{document_text[:8000]}

Identify:
1. High-Risk Items (could cause significant harm)
2. Medium-Risk Items (deserve attention)
3. Low-Risk Items (standard clauses)
4. Red Flags (immediate concerns)
5. Overall Risk Level (Low/Medium/High/Critical)

Be specific and cite the actual clause text."""

        risk_analysis = self._call_groq(prompt, max_tokens=2000)
        
        return {
            'risk_assessment': risk_analysis,
            'risk_level': self._extract_risk_level(risk_analysis)
        }
    
    def _extract_risk_level(self, analysis: str) -> str:
        """Extract overall risk level from analysis"""
        analysis_lower = analysis.lower()
        
        if 'critical' in analysis_lower or 'very high' in analysis_lower:
            return 'Critical'
        elif 'high risk' in analysis_lower or 'significant risk' in analysis_lower:
            return 'High'
        elif 'medium risk' in analysis_lower or 'moderate' in analysis_lower:
            return 'Medium'
        else:
            return 'Low'
    
    def answer_question(self, document_text: str, question: str) -> Dict:
        """Answer questions about the document"""
        prompt = f"""Based on this legal document, answer the following question.

Document:
{document_text[:6000]}

Question: {question}

Provide a clear, accurate answer. If the information isn't in the document, say so."""

        answer = self._call_groq(prompt, max_tokens=1000)
        
        return {
            'question': question,
            'answer': answer
        }
    
    def explain_clause(self, clause_text: str) -> Dict:
        """Explain a clause in plain English"""
        prompt = f"""Explain this legal clause in simple, plain English that anyone can understand.

Clause:
{clause_text}

Explain:
1. What it means
2. Why it matters
3. Potential implications
4. What to watch out for"""

        explanation = self._call_groq(prompt, max_tokens=800)
        
        return {
            'explanation': explanation
        }
    
    def compare_documents(self, doc1_text: str, doc2_text: str) -> Dict:
        """Compare two legal documents"""
        prompt = f"""Compare these two legal documents and highlight key differences.

Document 1:
{doc1_text[:3000]}

Document 2:
{doc2_text[:3000]}

Identify:
1. Main differences in terms
2. Which document is more favorable
3. Missing clauses in either document
4. Risk comparison"""

        comparison = self._call_groq(prompt, max_tokens=2000)
        
        return {
            'comparison': comparison
        }
    
    def analyze_complete(self, document_text: str) -> Dict:
        """Complete analysis pipeline"""
        try:
            # Get summary
            summary_result = self.summarize_document(document_text)
            
            # Get clauses
            clauses_result = self.extract_clauses(document_text)
            
            # Get risk assessment
            risk_result = self.assess_risks(document_text)
            
            return {
                'summary': summary_result,
                'clauses': clauses_result['clauses'],
                'risk_assessment': risk_result
            }
        except Exception as e:
            return {
                'error': str(e),
                'summary': {'summary': 'Error during analysis'},
                'clauses': 'Error extracting clauses',
                'risk_assessment': {'risk_assessment': 'Error assessing risks', 'risk_level': 'Unknown'}
            }
