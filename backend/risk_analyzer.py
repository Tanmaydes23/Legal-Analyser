"""
Risk Analyzer Module
Provides detailed risk analysis with ML-inspired scoring
Generates risk reports and visualizations
"""
from typing import Dict, List, Tuple
from dataclasses import dataclass
import json

@dataclass
class RiskFactor:
    """Represents a risk factor in the document"""
    category: str
    severity: str  # Critical, High, Medium, Low
    description: str
    impact: str
    mitigation: str
    clause_reference: str

class RiskAnalyzer:
    """Comprehensive risk analysis for legal documents"""
    
    # Risk patterns and indicators
    CRITICAL_PATTERNS = [
        'unlimited liability', 'perpetual', 'irrevocable', 
        'waive all rights', 'no recourse', 'sole discretion'
    ]
    
    HIGH_RISK_PATTERNS = [
        'non-compete', 'exclusive', 'indemnify', 'liquidated damages',
        'automatic renewal', 'unilateral', 'penalty'
    ]
    
    MEDIUM_RISK_PATTERNS = [
        'confidential', 'proprietary', 'termination', 'dispute',
        'amendment', 'assignment'
    ]
    
    def __init__(self):
        self.risk_factors = []
    
    def analyze_document_risk(self, document_text: str, clauses: List = None) -> Dict:
        """
        Perform comprehensive risk analysis
        Returns detailed risk report
        """
        # Identify risk factors
        risk_factors = self._identify_risk_factors(document_text)
        
        # Calculate overall risk score
        risk_score = self._calculate_risk_score(risk_factors)
        
        # Generate risk matrix
        risk_matrix = self._generate_risk_matrix(risk_factors)
        
        # Identify missing clauses
        missing_clauses = self._identify_missing_clauses(document_text)
        
        # Generate recommendations
        recommendations = self._generate_risk_recommendations(risk_factors, missing_clauses)
        
        return {
            'overall_risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'risk_factors': [self._risk_factor_to_dict(rf) for rf in risk_factors],
            'risk_matrix': risk_matrix,
            'missing_clauses': missing_clauses,
            'recommendations': recommendations,
            'summary': self._generate_risk_summary(risk_score, risk_factors)
        }
    
    def _identify_risk_factors(self, text: str) -> List[RiskFactor]:
        """Identify risk factors in document"""
        risk_factors = []
        text_lower = text.lower()
        
        # Check for critical risks
        for pattern in self.CRITICAL_PATTERNS:
            if pattern in text_lower:
                risk_factors.append(RiskFactor(
                    category='Critical Risk',
                    severity='Critical',
                    description=f'Document contains "{pattern}"',
                    impact='Could expose you to unlimited obligations or loss of rights',
                    mitigation='Strongly recommend legal review before signing',
                    clause_reference=self._find_clause_context(text, pattern)
                ))
        
        # Check for high risks
        for pattern in self.HIGH_RISK_PATTERNS:
            if pattern in text_lower:
                risk_factors.append(RiskFactor(
                    category='High Risk',
                    severity='High',
                    description=f'Contains restrictive "{pattern}" clause',
                    impact='May significantly limit your future options or increase liability',
                    mitigation='Negotiate terms or seek legal advice',
                    clause_reference=self._find_clause_context(text, pattern)
                ))
        
        # Check for medium risks
        for pattern in self.MEDIUM_RISK_PATTERNS:
            if pattern in text_lower:
                risk_factors.append(RiskFactor(
                    category='Standard Risk',
                    severity='Medium',
                    description=f'Standard "{pattern}" clause present',
                    impact='Common clause that requires attention',
                    mitigation='Review carefully to ensure terms are acceptable',
                    clause_reference=self._find_clause_context(text, pattern)
                ))
        
        return risk_factors[:15]  # Limit to top 15 risk factors
    
    def _find_clause_context(self, text: str, pattern: str, context_length: int = 200) -> str:
        """Find the context around a pattern"""
        text_lower = text.lower()
        index = text_lower.find(pattern.lower())
        
        if index == -1:
            return "Pattern not found"
        
        start = max(0, index - context_length // 2)
        end = min(len(text), index + len(pattern) + context_length // 2)
        
        context = text[start:end].strip()
        return f"...{context}..."
    
    def _calculate_risk_score(self, risk_factors: List[RiskFactor]) -> float:
        """
        Calculate overall risk score (0-100)
        100 = Highest risk
        """
        if not risk_factors:
            return 10.0  # Minimal risk if no factors found
        
        score = 0.0
        severity_weights = {
            'Critical': 25,
            'High': 15,
            'Medium': 8,
            'Low': 3
        }
        
        for factor in risk_factors:
            score += severity_weights.get(factor.severity, 5)
        
        # Cap at 100
        return min(100.0, score)
    
    def _get_risk_level(self, score: float) -> str:
        """Convert risk score to level"""
        if score >= 70:
            return 'Critical'
        elif score >= 50:
            return 'High'
        elif score >= 30:
            return 'Medium'
        else:
            return 'Low'
    
    def _generate_risk_matrix(self, risk_factors: List[RiskFactor]) -> Dict[str, int]:
        """Generate risk matrix breakdown"""
        matrix = {
            'Critical': 0,
            'High': 0,
            'Medium': 0,
            'Low': 0
        }
        
        for factor in risk_factors:
            matrix[factor.severity] += 1
        
        return matrix
    
    def _identify_missing_clauses(self, text: str) -> List[Dict[str, str]]:
        """Identify important clauses that should be present but aren't"""
        text_lower = text.lower()
        
        important_clauses = {
            'Limitation of Liability': ['limit', 'liability', 'cap'],
            'Termination for Convenience': ['terminate', 'convenience'],
            'Force Majeure': ['force majeure', 'act of god'],
            'Dispute Resolution': ['dispute', 'arbitration', 'mediation'],
            'Confidentiality': ['confidential', 'nda', 'non-disclosure'],
            'Intellectual Property': ['intellectual property', 'ip rights', 'ownership'],
        }
        
        missing = []
        for clause_name, keywords in important_clauses.items():
            if not any(keyword in text_lower for keyword in keywords):
                missing.append({
                    'clause': clause_name,
                    'importance': 'Important',
                    'reason': f'Should include {clause_name} to protect your interests'
                })
        
        return missing[:5]  # Top 5 missing clauses
    
    def _generate_risk_recommendations(self, risk_factors: List[RiskFactor], 
                                      missing_clauses: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Based on risk level
        critical_count = sum(1 for rf in risk_factors if rf.severity == 'Critical')
        high_count = sum(1 for rf in risk_factors if rf.severity == 'High')
        
        if critical_count > 0:
            recommendations.append('🚨 CRITICAL: Do NOT sign without legal review')
            recommendations.append('This document contains clauses that could significantly harm you')
        
        if high_count > 2:
            recommendations.append('⚠️ Multiple high-risk clauses detected')
            recommendations.append('Strongly recommend negotiating these terms')
        
        if missing_clauses:
            recommendations.append(f'Consider adding {len(missing_clauses)} important missing clauses')
        
        # Specific recommendations
        recommendations.extend([
            'Request modifications to unfavorable terms before signing',
            'Ask for definitions of ambiguous language',
            'Verify all dates, amounts, and obligations are correct',
            'Keep a signed copy for your records',
        ])
        
        return recommendations[:8]  # Top 8 recommendations
    
    def _generate_risk_summary(self, score: float, risk_factors: List[RiskFactor]) -> str:
        """Generate human-readable risk summary"""
        level = self._get_risk_level(score)
        
        summaries = {
            'Critical': f'⛔ CRITICAL RISK (Score: {score:.1f}/100) - This document contains severe risks that could expose you to significant liability or loss of rights. DO NOT SIGN without thorough legal review.',
            'High': f'⚠️ HIGH RISK (Score: {score:.1f}/100) - This document has multiple concerning clauses. Professional legal review strongly recommended before signing.',
            'Medium': f'⚡ MODERATE RISK (Score: {score:.1f}/100) - Standard contract with some potentially unfavorable terms. Review carefully and consider negotiation.',
            'Low': f'✅ LOW RISK (Score: {score:.1f}/100) - Generally favorable or standard terms. Review key obligations and dates before signing.'
        }
        
        return summaries.get(level, f'Risk Score: {score:.1f}/100')
    
    def _risk_factor_to_dict(self, rf: RiskFactor) -> Dict:
        """Convert RiskFactor to dictionary"""
        return {
            'category': rf.category,
            'severity': rf.severity,
            'description': rf.description,
            'impact': rf.impact,
            'mitigation': rf.mitigation,
            'clause_reference': rf.clause_reference
        }
    
    def generate_risk_heatmap_data(self, risk_factors) -> List[Dict]:
        """Generate data for risk heatmap visualization
        Accepts either List[RiskFactor] or List[Dict]"""
        heatmap_data = []
        
        categories = {}
        for rf in risk_factors:
            # Handle both dict and RiskFactor object
            category = rf['category'] if isinstance(rf, dict) else rf.category
            severity = rf['severity'] if isinstance(rf, dict) else rf.severity
            
            if category not in categories:
                categories[category] = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
            categories[category][severity] += 1
        
        for category, severities in categories.items():
            heatmap_data.append({
                'category': category,
                'severities': severities,
                'total': sum(severities.values())
            })
        
        return heatmap_data
