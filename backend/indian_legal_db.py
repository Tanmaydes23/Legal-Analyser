"""
Indian Legal Database Integration
Connects to Indian Kanoon API for case law and precedents
"""
import requests
from typing import Dict, List
import json

class IndianLegalDB:
    """Interface to Indian Kanoon legal database"""
    
    BASE_URL = "https://api.indiankanoon.org"
    
    def __init__(self):
        """Initialize Indian Kanoon client"""
        pass
    
    def search_cases(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search Indian case law
        
        Args:
            query: Search query (e.g., "breach of contract", "specific relief")
            max_results: Number of results to return
            
        Returns:
            List of relevant cases with citations
        """
        try:
            url = f"{self.BASE_URL}/search/"
            params = {
                'formInput': query,
                'pagenum': 0
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse results
            cases = []
            for result in data.get('docs', [])[:max_results]:
                cases.append({
                    'title': result.get('title', 'Untitled'),
                    'court': result.get('court', 'Unknown Court'),
                    'date': result.get('date', 'Unknown Date'),
                    'citation': result.get('citation', ''),
                    'tid': result.get('tid', ''),  # Unique ID
                    'url': f"https://indiankanoon.org/doc/{result.get('tid')}/" if result.get('tid') else '',
                    'snippet': result.get('headline', '')[:500]
                })
            
            return cases
        
        except Exception as e:
            print(f"Error searching Indian Kanoon: {str(e)}")
            return []
    
    def get_case_details(self, case_id: str) -> Dict:
        """
        Get full case details by ID
        
        Args:
            case_id: Indian Kanoon case ID (tid)
            
        Returns:
            Full case details including judgment text
        """
        try:
            url = f"{self.BASE_URL}/doc/{case_id}/"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
        
        except Exception as e:
            print(f"Error fetching case {case_id}: {str(e)}")
            return {}
    
    def find_relevant_precedents(self, clause_text: str, clause_type: str) -> List[Dict]:
        """
        Find relevant Indian legal precedents for a clause
        
        Args:
            clause_text: The clause text from user's document
            clause_type: Type of clause (e.g., 'termination', 'payment', 'liability')
            
        Returns:
            List of relevant Indian cases
        """
        # Construct search query based on clause type
        search_queries = {
            'termination': 'termination of contract specific relief',
            'payment': 'payment clause breach of contract',
            'liability': 'limitation of liability negligence',
            'indemnity': 'indemnity clause liability',
            'confidentiality': 'confidentiality agreement breach',
            'non_compete': 'non-compete agreement restraint of trade',
            'arbitration': 'arbitration clause validity',
            'force_majeure': 'force majeure act of god',
            'intellectual_property': 'intellectual property rights ownership',
            'warranty': 'warranty breach sale of goods'
        }
        
        query = search_queries.get(clause_type.lower(), clause_type)
        
        # Search for precedents
        return self.search_cases(query, max_results=5)
    
    def analyze_with_precedents(self, document_text: str, clauses: List) -> Dict:
        """
        Analyze document with Indian legal precedents
        
        Args:
            document_text: Full document text
            clauses: Extracted clauses from document
            
        Returns:
            Analysis with relevant Indian case law
        """
        analysis = {
            'precedents_found': [],
            'jurisdiction': 'India',
            'relevant_acts': self._identify_relevant_acts(document_text),
            'case_law_summary': ''
        }
        
        # Find precedents for high-risk clauses
        for clause in clauses[:5]:  # Top 5 clauses
            if hasattr(clause, 'type'):
                precedents = self.find_relevant_precedents(
                    clause.text if hasattr(clause, 'text') else str(clause),
                    clause.type
                )
                
                if precedents:
                    analysis['precedents_found'].extend(precedents)
        
        # Remove duplicates
        seen = set()
        unique_precedents = []
        for p in analysis['precedents_found']:
            tid = p.get('tid', '')
            if tid and tid not in seen:
                seen.add(tid)
                unique_precedents.append(p)
        
        analysis['precedents_found'] = unique_precedents[:10]  # Top 10
        
        return analysis
    
    def _identify_relevant_acts(self, text: str) -> List[str]:
        """Identify relevant Indian Acts mentioned or applicable"""
        text_lower = text.lower()
        
        relevant_acts = []
        
        # Common Indian Acts
        act_indicators = {
            'Indian Contract Act, 1872': ['contract', 'agreement', 'consideration'],
            'Sale of Goods Act, 1930': ['sale', 'goods', 'buyer', 'seller'],
            'Specific Relief Act, 1963': ['specific performance', 'injunction', 'rescission'],
            'Arbitration and Conciliation Act, 1996': ['arbitration', 'arbitrator', 'dispute resolution'],
            'Information Technology Act, 2000': ['data', 'electronic', 'cyber', 'digital'],
            'Consumer Protection Act, 2019': ['consumer', 'deficiency in service'],
            'Companies Act, 2013': ['company', 'director', 'shareholder'],
            'Employment Act': ['employment', 'employee', 'employer', 'termination'],
            'Copyright Act, 1957': ['copyright', 'intellectual property', 'original work'],
            'Patents Act, 1970': ['patent', 'invention', 'patentee']
        }
        
        for act, keywords in act_indicators.items():
            if any(keyword in text_lower for keyword in keywords):
                relevant_acts.append(act)
        
        return relevant_acts[:5]  # Top 5 most relevant


# Example usage
if __name__ == "__main__":
    db = IndianLegalDB()
    
    # Test search
    print("Searching for contract breach cases...")
    cases = db.search_cases("breach of contract")
    
    for case in cases[:3]:
        print(f"\n{case['title']}")
        print(f"Court: {case['court']}")
        print(f"Date: {case['date']}")
        print(f"URL: {case['url']}")
        print(f"Snippet: {case['snippet'][:200]}...")
