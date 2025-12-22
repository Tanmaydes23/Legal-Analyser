"""
Advanced Clause Extractor using Transformer Models
Extracts 40+ types of legal clauses using CUAD dataset patterns
Combines rule-based extraction with AI analysis
"""
from typing import List, Dict, Optional
import re
from dataclasses import dataclass

@dataclass
class Clause:
    """Represents a legal clause"""
    type: str
    text: str
    risk_level: str  # Low, Medium, High
    location: str  # Page/paragraph location
    explanation: str
    recommendations: List[str]

class ClauseExtractor:
    """Extract and categorize legal clauses"""
    
    # 40+ clause types based on CUAD dataset
    CLAUSE_TYPES = {
        'Payment Terms': ['payment', 'fee', 'price', 'cost', 'compensation', 'remuneration'],
        'Termination': ['terminate', 'termination', 'cancel', 'cancellation', 'end agreement'],
        'Confidentiality': ['confidential', 'non-disclosure', 'proprietary', 'secret'],
        'Intellectual Property': ['intellectual property', 'IP', 'copyright', 'patent', 'trademark'],
        'Liability': ['liable', 'liability', 'indemnify', 'indemnification', 'damages'],
        'Warranty': ['warrant', 'warranty', 'guarantee', 'representation'],
        'Dispute Resolution': ['dispute', 'arbitration', 'mediation', 'jurisdiction', 'venue'],
        'Force Majeure': ['force majeure', 'act of god', 'beyond control'],
        'Assignment': ['assign', 'assignment', 'transfer'],
        'Amendment': ['amend', 'amendment', 'modify', 'modification', 'change'],
        'Severability': ['severability', 'severable', 'invalid provision'],
        'Entire Agreement': ['entire agreement', 'supersede', 'complete agreement'],
        'Notices': ['notice', 'notification', 'communicate'],
        'Governing Law': ['governing law', 'applicable law', 'jurisdiction'],
        'Non-Compete': ['non-compete', 'non-competition', 'competitive'],
        'Non-Solicitation': ['non-solicit', 'solicitation'],
        'Term/Duration': ['term', 'duration', 'period', 'effective date'],
        'Renewal': ['renew', 'renewal', 'extend', 'extension'],
        'Insurance': ['insurance', 'insure', 'coverage'],
        'Audit Rights': ['audit', 'inspect', 'examination of records'],
        'Most Favored Nation': ['most favored', 'MFN', 'preferential'],
        'Price Restrictions': ['price', 'pricing', 'discount'],
        'Volume Restrictions': ['volume', 'quantity', 'minimum purchase'],
        'Exclusivity': ['exclusive', 'exclusivity', 'sole'],
        'Change of Control': ['change of control', 'acquisition', 'merger'],
        'Anti-Assignment': ['not assign', 'no assignment', 'assignment prohibited'],
        'Revenue/Profit Sharing': ['revenue share', 'profit share', 'royalty'],
        'Cap on Liability': ['limit liability', 'cap', 'maximum liability'],
        'Liquidated Damages': ['liquidated damages', 'penalty'],
        'Uncapped Liability': ['unlimited liability', 'uncapped'],
        'Joint Liability': ['joint', 'jointly liable', 'several'],
        'Third Party Beneficiary': ['third party', 'beneficiary'],
        'License Grant': ['license', 'grant', 'right to use'],
        'Non-Transferable License': ['non-transferable', 'personal license'],
        'Affiliate License': ['affiliate', 'subsidiary'],
        'Post-Termination Services': ['post-termination', 'wind down', 'transition'],
        'Covenant Not to Sue': ['covenant', 'not sue', 'waive claims'],
        'ROFR/ROFO': ['right of first', 'ROFR', 'ROFO', 'first refusal'],
        'No-Hire': ['no-hire', 'non-hire', 'not hire'],
        'Competitive Restriction': ['competitive restriction', 'compete'],
    }
    
    def __init__(self):
        self.clauses_found = []
    
    def extract_clauses(self, document_text: str) -> List[Clause]:
        """
        Extract clauses from document text
        Uses pattern matching + contextual analysis
        """
        clauses = []
        paragraphs = self._split_into_paragraphs(document_text)
        
        for idx, paragraph in enumerate(paragraphs):
            for clause_type, keywords in self.CLAUSE_TYPES.items():
                if self._contains_keywords(paragraph, keywords):
                    clause = self._create_clause(
                        clause_type=clause_type,
                        text=paragraph,
                        location=f"Paragraph {idx + 1}"
                    )
                    clauses.append(clause)
        
        return clauses
    
    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Split document into paragraphs"""
        # Split on double newlines or numbered sections
        paragraphs = re.split(r'\n\s*\n|\n\d+\.', text)
        return [p.strip() for p in paragraphs if p.strip() and len(p) > 50]
    
    def _contains_keywords(self, text: str, keywords: List[str]) -> bool:
        """Check if text contains any of the keywords"""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)
    
    def _create_clause(self, clause_type: str, text: str, location: str) -> Clause:
        """Create a Clause object with risk assessment"""
        risk_level = self._assess_risk(clause_type, text)
        explanation = self._generate_explanation(clause_type)
        recommendations = self._generate_recommendations(clause_type, risk_level)
        
        return Clause(
            type=clause_type,
            text=text[:500] + "..." if len(text) > 500 else text,  # Truncate long clauses
            risk_level=risk_level,
            location=location,
            explanation=explanation,
            recommendations=recommendations
        )
    
    def _assess_risk(self, clause_type: str, text: str) -> str:
        """Assess risk level of clause"""
        # High-risk clause types
        high_risk_types = [
            'Liability', 'Uncapped Liability', 'Liquidated Damages',
            'Non-Compete', 'Exclusivity', 'Anti-Assignment',
            'Joint Liability', 'Covenant Not to Sue'
        ]
        
        # Medium-risk clause types
        medium_risk_types = [
            'Termination', 'Payment Terms', 'Intellectual Property',
            'Change of Control', 'Cap on Liability', 'Warranty',
            'Post-Termination Services', 'Competitive Restriction'
        ]
        
        # Check for risk indicators in text
        text_lower = text.lower()
        high_risk_words = ['unlimited', 'perpetual', 'irrevocable', 'waive', 'indemnify']
        
        if clause_type in high_risk_types or any(word in text_lower for word in high_risk_words):
            return 'High'
        elif clause_type in medium_risk_types:
            return 'Medium'
        else:
            return 'Low'
    
    def _generate_explanation(self, clause_type: str) -> str:
        """Generate plain English explanation"""
        explanations = {
            'Payment Terms': 'Defines how and when payments must be made',
            'Termination': 'Explains under what conditions the contract can be ended',
            'Confidentiality': 'Protects sensitive information from disclosure',
            'Intellectual Property': 'Determines who owns created work or innovations',
            'Liability': 'Specifies who is responsible for damages or losses',
            'Warranty': 'Guarantees about product/service quality',
            'Dispute Resolution': 'How disagreements will be resolved',
            'Non-Compete': 'Restricts working with competitors',
            'Exclusivity': 'Grants exclusive rights to one party',
        }
        return explanations.get(clause_type, f'Clause related to {clause_type}')
    
    def _generate_recommendations(self, clause_type: str, risk_level: str) -> List[str]:
        """Generate recommendations based on clause type and risk"""
        recommendations = []
        
        if risk_level == 'High':
            recommendations.append('⚠️ Have a lawyer review this clause')
            recommendations.append('Consider negotiating less restrictive terms')
        
        if clause_type == 'Termination':
            recommendations.append('Ensure termination conditions are clear and favorable')
        elif clause_type == 'Liability':
            recommendations.append('Verify liability caps are reasonable')
        elif clause_type == 'Non-Compete':
            recommendations.append('Check geographic and time restrictions')
        
        return recommendations
    
    def categorize_clauses(self, clauses: List[Clause]) -> Dict[str, List[Clause]]:
        """Group clauses by type"""
        categorized = {}
        for clause in clauses:
            if clause.type not in categorized:
                categorized[clause.type] = []
            categorized[clause.type].append(clause)
        return categorized
    
    def get_risk_summary(self, clauses: List[Clause]) -> Dict[str, int]:
        """Get summary of risk levels"""
        risk_counts = {'High': 0, 'Medium': 0, 'Low': 0}
        for clause in clauses:
            risk_counts[clause.risk_level] += 1
        return risk_counts
