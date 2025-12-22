"""
LLM-Based Risk Assessor
Uses Groq LLM for intelligent risk assessment instead of hardcoded rules
Replaces rule-based risk logic with AI-powered analysis
"""
from typing import Dict, List, Optional
from ai_analyzer import LegalAIAnalyzer


class LLMRiskAssessor:
    """
    LLM-based risk assessment replacing hardcoded rules
    Uses Groq LLM with India-specific prompts
    """
    
    def __init__(self):
        """Initialize LLM risk assessor"""
        print("🧠 Initializing LLM-Based Risk Assessor...")
        self.llm = LegalAIAnalyzer()
        print("   ✅ LLM Risk Assessor ready")
    
    def assess_clause_risk(self, clause: Dict, entities: List[Dict], applicable_acts: List[Dict]) -> Dict:
        """
        Assess risk of a single clause using LLM
        
        Args:
            clause: Clause data with text, type, etc.
            entities: Extracted entities from the clause
            applicable_acts: List of applicable Indian Acts
            
        Returns:
            Risk assessment with level, reason, recommendations
        """
        clause_text = clause.get('text', '')
        clause_type = clause.get('type', 'general')
        
        # Prepare entities summary
        entities_str = self._format_entities(entities)
        acts_str = ', '.join([act.get('name', '') for act in applicable_acts])
        
        # LLM prompt for risk assessment
        prompt = f"""You are an expert in Indian contract law. Analyze this clause for RISK.

CLAUSE TYPE: {clause_type}

CLAUSE TEXT:
{clause_text}

ENTITIES FOUND:
{entities_str}

APPLICABLE INDIAN LAWS:
{acts_str}

Assess the risk level considering:
1. Indian Contract Act, 1872
2. TDS requirements (Income Tax Act)
3. GST compliance (GST Act 2017)
4. Stamp duty requirements
5. Indian jurisdiction and enforceability
6. Common pitfalls in Indian contracts

Output JSON format:
{{
    "risk_level": "Low|Medium|High|Critical",
    "risk_score": 0-100,
    "risk_factors": ["factor 1", "factor 2"],
    "reason": "Brief explanation",
    "indian_law_issues": ["issue 1", "issue 2"]
}}

Output ONLY the JSON, no additional text."""

        try:
            response = self.llm._call_groq(prompt, max_tokens=500)
            
            # Parse JSON response
            import json
            risk_data = json.loads(response)
            
            return {
                'risk_level': risk_data.get('risk_level', 'Medium'),
                'risk_score': risk_data.get('risk_score', 50),
                'risk_factors': risk_data.get('risk_factors', []),
                'reason': risk_data.get('reason', 'LLM analysis'),
                'indian_law_issues': risk_data.get('indian_law_issues', []),
                'method': 'LLM-based (Groq)'
            }
            
        except Exception as e:
            print(f"   ⚠️ LLM risk assessment error: {str(e)}")
            # Fallback to medium risk
            return {
                'risk_level': 'Medium',
                'risk_score': 50,
                'risk_factors': ['LLM assessment failed'],
                'reason': 'Could not complete LLM analysis',
                'indian_law_issues': [],
                'method': 'Fallback'
            }
    
    def assess_batch_clauses(self, clauses: List[Dict], entities_by_clause: Dict, 
                           applicable_acts: List[Dict]) -> List[Dict]:
        """
        Assess risk for multiple clauses in one batch LLM call (more efficient)
        
        Args:
            clauses: List of clause dicts
            entities_by_clause: Dict mapping clause index to entities
            applicable_acts: List of applicable acts
            
        Returns:
            List of risk assessments for each clause
        """
        # Format all clauses for batch processing
        clauses_summary = []
        for i, clause in enumerate(clauses[:
20]):  # Limit to 20 for token limits
            entities = entities_by_clause.get(i, [])
            clauses_summary.append({
                'index': i,
                'type': clause.get('type', 'general'),
                'text': clause.get('text', '')[:200],  # Truncate long clauses
                'entities': [e.get('text', '') for e in entities[:5]]
            })
        
        acts_str = ', '.join([act.get('name', '') for act in applicable_acts])
        
        prompt = f"""You are an expert in Indian contract law. Analyze these clauses for RISK in batch.

APPLICABLE INDIAN LAWS: {acts_str}

CLAUSES TO ANALYZE:
{json.dumps(clauses_summary, indent=2)}

For each clause, assess risk considering:
- Indian Contract Act, 1872
- TDS/GST compliance
- Stamp duty requirements
- Indian jurisdiction
- Common contract pitfalls in India

Output JSON array format (one entry per clause):
[
    {{
        "index": 0,
        "risk_level": "Low|Medium|High|Critical",
        "risk_score": 0-100,
        "key_issue": "Brief description"
    }},
    ...
]

Output ONLY the JSON array, no additional text."""

        try:
            import json
            response = self.llm._call_groq(prompt, max_tokens=1500)
            risk_results = json.loads(response)
            
            # Map results back to clauses
            assessments = []
            for result in risk_results:
                idx = result.get('index', len(assessments))
                assessments.append({
                    'risk_level': result.get('risk_level', 'Medium'),
                    'risk_score': result.get('risk_score', 50),
                    'key_issue': result.get('key_issue', ''),
                    'method': 'LLM-batch'
                })
            
            # Fill in missing assessments
            while len(assessments) < len(clauses):
                assessments.append({
                    'risk_level': 'Medium',
                    'risk_score': 50,
                    'key_issue': 'Batch processing incomplete',
                    'method': 'Fallback'
                })
            
            return assessments[:len(clauses)]
            
        except Exception as e:
            print(f"   ⚠️ Batch risk assessment error: {str(e)}")
            # Fallback: all medium risk
            return [{
                'risk_level': 'Medium',
                'risk_score': 50,
                'key_issue': 'Batch assessment failed',
                'method': 'Fallback'
            } for _ in clauses]
    
    def detect_missing_clauses(self, found_clauses: List[Dict], document_type: str,
                              applicable_acts: List[Dict], document_text: str) -> Dict:
        """
        Use LLM to detect missing mandatory clauses
        
        Args:
            found_clauses: List of clauses found by InLegalBERT
            document_type: Type of document (service_agreement, employment, etc.)
            applicable_acts: Applicable Indian Acts
            document_text: Full document text (first 2000 chars)
            
        Returns:
            Missing clauses analysis
        """
        clause_types_found = [c.get('type', '') for c in found_clauses]
        acts_str = ', '.join([act.get('name', '') for act in applicable_acts])
        
        prompt = f"""You are an expert in Indian contract law. Identify MISSING mandatory clauses.

DOCUMENT TYPE: {document_type}

CLAUSES FOUND IN DOCUMENT:
{', '.join(clause_types_found)}

APPLICABLE INDIAN LAWS:
{acts_str}

DOCUMENT PREVIEW:
{document_text[:2000]}

What MANDATORY clauses are MISSING for this {document_type} under Indian law?
Consider:
1. TDS provisions (Income Tax Act) - mandatory for service payments
2. GST provisions (GST Act 2017) - mandatory for most transactions
3. Stamp duty mention (Indian Stamp Act)
4. Termination clause
5. Governing law and jurisdiction (should be Indian)
6. Arbitration/dispute resolution
7. Other India-specific requirements

Output JSON format:
{{
    "missing_clauses": [
        {{
            "clause_type": "tds_clause",
            "importance": "High|Medium",
            "reason": "Why it's needed",
            "legal_basis": "Which Indian law requires it"
        }}
    ],
    "compliance_score": 0-100,
    "critical_gaps": ["gap 1", "gap 2"]
}}

Output ONLY the JSON, no additional text."""

        try:
            import json
            response = self.llm._call_groq(prompt, max_tokens=800)
            missing_data = self._extract_json(response)
            
            if missing_data:
                return {
                    'missing_clauses': missing_data.get('missing_clauses', []),
                    'compliance_score': missing_data.get('compliance_score', 50),
                    'critical_gaps': missing_data.get('critical_gaps', []),
                    'method': 'LLM-based detection'
                }
            else:
                raise ValueError("No valid JSON in response")
            
        except Exception as e:
            print(f"   ⚠️ Missing clause detection error: {str(e)}")
            return {
                'missing_clauses': [],
                'compliance_score': 50,
                'critical_gaps': ['Could not complete LLM analysis'],
                'method': 'Fallback'
            }
    
    def check_indian_compliance(self, document_text: str, clauses: List[Dict],
                               applicable_acts: List[Dict]) -> Dict:
        """
        LLM-based Indian compliance checking
        
        Args:
            document_text: Full document text
            clauses: All extracted clauses
            applicable_acts: Applicable acts
            
        Returns:
            Compliance analysis
        """
        acts_str = ', '.join([act.get('name', '') for act in applicable_acts])
        
        prompt = f"""You are an expert in Indian contract law compliance. Check this contract for Indian legal compliance.

APPLICABLE INDIAN LAWS:
{acts_str}

DOCUMENT PREVIEW:
{document_text[:2500]}

Compliance checklist for Indian contracts:
1. TDS provisions mentioned?
2. GST provisions clear?
3. Indian jurisdiction specified?
4. Stamp duty addressed?
5. Complies with Indian Contract Act 1872?
6. Any India-specific regulatory requirements?

Output JSON format:
{{
    "compliance_checks": {{
        "tds_mentioned": true|false,
        "gst_mentioned": true|false,
        "indian_jurisdiction": true|false,
        "stamp_duty_mentioned": true|false,
        "contract_act_compliant": true|false
    }},
    "compliance_score": 0-100,
    "compliance_issues": ["issue 1", "issue 2"],
    "recommendations": ["recommendation 1", "recommendation 2"]
}}

Output ONLY the JSON, no additional text."""

        try:
            import json
            response = self.llm._call_groq(prompt, max_tokens=700)
            compliance_data = self._extract_json(response)
            
            if compliance_data:
                return {
                    'compliance_checks': compliance_data.get('compliance_checks', {}),
                    'compliance_score': compliance_data.get('compliance_score', 50),
                    'compliance_issues': compliance_data.get('compliance_issues', []),
                    'recommendations': compliance_data.get('recommendations', []),
                    'method': 'LLM-based compliance check'
                }
            else:
                raise ValueError("No valid JSON in response")
            
        except Exception as e:
            print(f"   ⚠️ Compliance check error: {str(e)}")
            return {
                'compliance_checks': {},
                'compliance_score': 50,
                'compliance_issues': ['Could not complete LLM analysis'],
                'recommendations': [],
                'method': 'Fallback'
            }
    
    def _extract_json(self, response: str) -> Optional[Dict]:
        """Extract JSON from LLM response, handling markdown code blocks"""
        import json
        import re
        
        if not response or not response.strip():
            return None
        
        try:
            # Try direct JSON parse first
            return json.loads(response)
        except:
            pass
        
        # Try extracting from markdown code block
        json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except:
                pass
        
        # Try finding any JSON object
        json_match = re.search(r'{.*}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except:
                pass
        
        return None
    
    def _format_entities(self, entities: List[Dict]) -> str:
        """Format entities for LLM prompt"""
        if not entities:
            return "No entities extracted"
        
        formatted = []
        for e in entities[:10]:  # Limit to 10
            formatted.append(f"- {e.get('type', 'UNKNOWN')}: {e.get('text', '')}")
        
        return '\n'.join(formatted)


# Singleton
_llm_assessor_instance = None

def get_llm_risk_assessor() -> LLMRiskAssessor:
    """Get or create LLM risk assessor instance"""
    global _llm_assessor_instance
    if _llm_assessor_instance is None:
        _llm_assessor_instance = LLMRiskAssessor()
    return _llm_assessor_instance
