"""
Indian Legal Knowledge Base
Contains Indian-specific legal information, acts, and compliance requirements
"""
from typing import Dict, List, Set
from dataclasses import dataclass

@dataclass
class IndianAct:
    """Represents an Indian legal act"""
    name: str
    year: int
    short_name: str
    key_sections: Dict[str, str]
    keywords: List[str]

class IndianLegalKB:
    """Indian Legal Knowledge Base"""
    
    def __init__(self):
        """Initialize Indian legal knowledge"""
        self.acts = self._load_indian_acts()
        self.clause_types = self._load_indian_clause_types()
        self.compliance_requirements = self._load_compliance_requirements()
        self.legal_terms = self._load_indian_legal_terms()
    
    def _load_indian_acts(self) -> Dict[str, IndianAct]:
        """Load major Indian Acts"""
        return {
            'contract_act': IndianAct(
                name="Indian Contract Act",
                year=1872,
                short_name="ICA 1872",
                key_sections={
                    '10': 'What agreements are contracts',
                    '23': 'Void agreements - unlawful consideration',
                    '64': 'Consequences of rescission of voidable contract',
                    '73': 'Compensation for loss or damage caused by breach'
                },
                keywords=['contract', 'agreement', 'consideration', 'void', 'voidable']
            ),
            'specific_relief': IndianAct(
                name="Specific Relief Act",
                year=1963,
                short_name="SRA 1963",
                key_sections={
                    '10': 'Cases in which specific performance enforceable',
                    '14': 'Contracts not specifically enforceable',
                    '20': 'Discretion as to decreeing specific performance'
                },
                keywords=['specific performance', 'injunction', 'rescission']
            ),
            'sale_of_goods': IndianAct(
                name="Sale of Goods Act",
                year=1930,
                short_name="SOGA 1930",
                key_sections={
                    '4': 'Sale and agreement to sell',
                    '16': 'Goods must be ascertained',
                    '54': 'Liability of buyer for neglecting to take delivery'
                },
                keywords=['sale', 'goods', 'buyer', 'seller', 'delivery', 'warranty']
            ),
            'arbitration': IndianAct(
                name="Arbitration and Conciliation Act",
                year=1996,
                short_name="A&C Act 1996",
                key_sections={
                    '7': 'Arbitration agreement',
                    '11': 'Appointment of arbitrators',
                    '34': 'Setting aside arbitral award'
                },
                keywords=['arbitration', 'arbitrator', 'arbitral award', 'dispute resolution']
            ),
            'it_act': IndianAct(
                name="Information Technology Act",
                year=2000,
                short_name="IT Act 2000",
                key_sections={
                    '43': 'Penalty for damage to computer system',
                    '66': 'Computer related offences',
                    '72': 'Breach of confidentiality and privacy'
                },
                keywords=['data', 'electronic', 'cyber', 'digital', 'privacy', 'breach']
            ),
            'consumer_protection': IndianAct(
                name="Consumer Protection Act",
                year=2019,
                short_name="CPA 2019",
                key_sections={
                    '2': 'Definitions - consumer, deficiency',
                    '34': 'Jurisdiction of District Commission',
                    '58': 'Consumer disputes redressal'
                },
                keywords=['consumer', 'deficiency', 'unfair trade practice']
            ),
            'companies_act': IndianAct(
                name="Companies Act",
                year=2013,
                short_name="Companies Act 2013",
                key_sections={
                    '2': 'Definitions',
                    '149': 'Company to have Board of Directors',
                    '230': 'Power to compromise or make arrangements'
                },
                keywords=['company', 'director', 'shareholder', 'board', 'members']
            )
        }
    
    def _load_indian_clause_types(self) -> Dict[str, Dict]:
        """Load Indian-specific clause types and patterns"""
        return {
            'payment': {
                'description': 'Payment terms, fees, compensation',
                'keywords': ['payment', 'fee', 'salary', 'remuneration', 'rupees', '₹', 'consideration'],
                'risk_indicators': ['advance payment', 'no refund', 'late payment penalty'],
                'indian_context': 'Subject to TDS under Income Tax Act'
            },
            'termination': {
                'description': 'Contract termination and exit clauses',
                'keywords': ['termination', 'cancellation', 'notice period', 'exit'],
                'risk_indicators': ['immediate termination', 'no notice', 'unilateral'],
                'indian_context': 'Must comply with Industrial Disputes Act for employment'
            },
            'liability': {
                'description': 'Limitation of liability and indemnity',
                'keywords': ['liable', 'liability', 'indemnify', 'damages', 'loss'],
                'risk_indicators': ['unlimited liability', 'no cap', 'consequential damages'],
                'indian_context': 'Cannot exclude liability for gross negligence'
            },
            'confidentiality': {
                'description': 'Non-disclosure and confidentiality obligations',
                'keywords': ['confidential', 'non-disclosure', 'NDA', 'trade secret', 'proprietary'],
                'risk_indicators': ['perpetual', 'no exceptions', 'broad definition'],
                'indian_context': 'Protected under IT Act 2000 Section 72'
            },
            'arbitration': {
                'description': 'Dispute resolution through arbitration',
                'keywords': ['arbitration', 'arbitrator', 'dispute resolution', 'mediation'],
                'risk_indicators': ['foreign arbitration', 'costs on losing party'],
                'indian_context': 'Governed by Arbitration Act 1996; Delhi/Mumbai seats common'
            },
            'force_majeure': {
                'description': "Act of God and force majeure events",
                'keywords': ['force majeure', 'act of god', 'pandemic', 'war', 'natural disaster'],
                'risk_indicators': ['narrow definition', 'no relief', 'immediate termination'],
                'indian_context': 'Recognized under Section 56 of Indian Contract Act'
            },
            'intellectual_property': {
                'description': 'IP ownership and licensing',
                'keywords': ['intellectual property', 'copyright', 'patent', 'trademark', 'IP'],
                'risk_indicators': ['full transfer', 'perpetual license', 'no attribution'],
                'indian_context': 'Copyright Act 1957, Patents Act 1970 applicable'
            },
            'governing_law': {
                'description': 'Jurisdiction and governing law',
                'keywords': ['governing law', 'jurisdiction', 'courts of', 'Indian law'],
                'risk_indicators': ['foreign jurisdiction', 'foreign law', 'arbitration abroad'],
                'indian_context': 'Indian courts preferred; specify city/state'
            },
            'stamp_duty': {
                'description': 'Stamp duty and registration (India-specific)',
                'keywords': ['stamp duty', 'stamp paper', 'registration', 'registered document'],
                'risk_indicators': ['unstamped', 'insufficient stamp duty'],
                'indian_context': 'Mandatory under Indian Stamp Act; varies by state'
            },
            'tds_clause': {
                'description': 'Tax deduction at source (India-specific)',
                'keywords': ['TDS', 'tax deduction', 'withholding tax', 'income tax'],
                'risk_indicators': ['no TDS provision', 'unclear responsibility'],
                'indian_context': 'Mandatory under Income Tax Act for specified payments'
            },
            'gst_provision': {
                'description': 'GST applicability (India-specific)',
                'keywords': ['GST', 'goods and services tax', 'IGST', 'CGST', 'SGST'],
                'risk_indicators': ['GST not mentioned', 'unclear GST responsibility'],
                'indian_context': 'Applicable on most services since July 2017'
            }
        }
    
    def _load_compliance_requirements(self) -> Dict[str, List[str]]:
        """Load Indian compliance checklists"""
        return {
            'employment_contract': [
                'Notice period must be reasonable (30-90 days standard)',
                'Gratuity provisions if 5+ years employment',
                'PF/ESI deductions mentioned if applicable',
                'Form 16 issuance for tax purposes',
                'Comply with state labor laws'
            ],
            'service_agreement': [
                'TDS clause for payments above threshold',
                'GST provisions clearly stated',
                'Payment terms in Indian Rupees',
                'Indian jurisdiction specified',
                'Stamp duty compliance'
            ],
            'sales_contract': [
                'Delivery and title transfer clarified',
                'Warranty provisions as per SOGA 1930',
                'Dispute resolution mechanism',
                'Payment terms with GST',
                'Jurisdiction clause'
            ],
            'license_agreement': [
                'IP ownership clearly defined',
                'License scope and limitations',
                'Termination and post-termination rights',
                'Confidentiality obligations',
                'Indian law compliance'
            ]
        }
    
    def _load_indian_legal_terms(self) -> Dict[str, str]:
        """Load Indian legal terminology"""
        return {
            'petitioner': 'Party who files a petition/writ',
            'respondent': 'Party against whom petition is filed',
            'writ': 'Order by High Court or Supreme Court',
            'pil': 'Public Interest Litigation',
            'cause_of_action': 'Facts giving rise to legal claim',
            'decree': 'Formal expression of court adjudication',
            'honble': 'Honorable (used for judges/courts)',
            'interim_relief': 'Temporary relief pending final decision',
            'stay_order': 'Suspension of proceedings',
            'vakalatnama': 'Power of attorney for legal representation'
        }
    
    def identify_applicable_acts(self, text: str) -> List[IndianAct]:
        """Identify which Indian Acts are applicable"""
        text_lower = text.lower()
        applicable = []
        
        for act in self.acts.values():
            if any(keyword in text_lower for keyword in act.keywords):
                applicable.append(act)
        
        return applicable
    
    def get_clause_info(self, clause_type: str) -> Dict:
        """Get information about a clause type"""
        return self.clause_types.get(clause_type.lower(), {})
    
    def get_compliance_checklist(self, document_type: str) -> List[str]:
        """Get compliance checklist for document type"""
        return self.compliance_requirements.get(document_type.lower(), [])
    
    def is_indian_specific_clause(self, clause_type: str) -> bool:
        """Check if clause is India-specific"""
        indian_specific = {'stamp_duty', 'tds_clause', 'gst_provision'}
        return clause_type.lower() in indian_specific
