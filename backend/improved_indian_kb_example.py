"""
Example: Replace hardcoded Indian Legal KB with civictech-India JSON data

This demonstrates how to use real, community-maintained datasets instead of hardcoded data.
"""
import requests
import json
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class IndianAct:
    """Represents an Indian legal act"""
    name: str
    year: int
    short_name: str
    sections: List[Dict]  # Changed from key_sections
    keywords: List[str]


class ImprovedIndianLegalKB:
    """
    Indian Legal KB using externally sourced data instead of hardcoding.
    
    Sources:
    - Acts: civictech-India GitHub (https://github.com/civictech-India/Indian-Law-Penal-Code-Json)
    - Can be extended with OpenNyAI, Indian Kanoon API, etc.
    """
    
    def __init__(self, use_cached=True):
        """
        Initialize with external data sources
        
        Args:
            use_cached: If True, download and cache JSONs locally
        """
        self.cache_dir = "./legal_data_cache"
        self.use_cached = use_cached
        
        # Data sources
        self.github_base = "https://raw.githubusercontent.com/civictech-India/Indian-Law-Penal-Code-Json/master"
        
        # Load data from external sources
        self.acts = self._load_acts_from_github()
        self.clause_types = self._load_indian_clause_types()  # Can still be local or from another source
        
        print(f"✅ Loaded {len(self.acts)} acts from external sources")
    
    def _load_acts_from_github(self) -> Dict[str, IndianAct]:
        """
        Load Indian Acts from civictech-India GitHub repository
        Much better than hardcoding!
        """
        acts_urls = {
            'ipc': f"{self.github_base}/ipc.json",
            'crpc': f"{self.github_base}/crpc.json", 
            'cpc': f"{self.github_base}/cpc.json",
            'hma': f"{self.github_base}/hma.json",
            'ida': f"{self.github_base}/ida.json",
            'iea': f"{self.github_base}/iea.json",
            'nia': f"{self.github_base}/nia.json",
            'mva': f"{self.github_base}/mva.json",
        }
        
        acts_data = {}
        
        for act_key, url in acts_urls.items():
            try:
                print(f"   Downloading {act_key.upper()}...")
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Convert to IndianAct format
                    act = self._convert_github_json_to_act(act_key, data)
                    acts_data[act_key] = act
                    print(f"   ✅ {act.name} loaded ({len(act.sections)} sections)")
                else:
                    print(f"   ❌ Failed to load {act_key}: {response.status_code}")
                    
            except Exception as e:
                print(f"   ⚠️ Error loading {act_key}: {str(e)}")
                continue
        
        return acts_data
    
    def _convert_github_json_to_act(self, act_key: str, data: Dict) -> IndianAct:
        """Convert civictech-India JSON format to our IndianAct format"""
        
        # Extract metadata (structure varies by act)
        act_name = data.get('title', act_key.upper())
        year = data.get('year', 0)
        
        # Extract sections
        sections = []
        if 'sections' in data:
            sections = data['sections']
        elif 'chapters' in data:
            # Some acts have chapters containing sections
            for chapter in data['chapters']:
                if 'sections' in chapter:
                    sections.extend(chapter['sections'])
        
        # Generate keywords based on act type
        keywords = self._generate_keywords_for_act(act_key, act_name)
        
        return IndianAct(
            name=act_name,
            year=year,
            short_name=f"{act_key.upper()} {year}",
            sections=sections,
            keywords=keywords
        )
    
    def _generate_keywords_for_act(self, act_key: str, act_name: str) -> List[str]:
        """Generate search keywords for each act"""
        keyword_mapping = {
            'ipc': ['murder', 'theft', 'assault', 'criminal', 'offence', 'punishment'],
            'crpc': ['arrest', 'bail', 'trial', 'procedure', 'investigation'],
            'cpc': ['suit', 'decree', 'civil', 'plaintiff', 'defendant', 'judgment'],
            'hma': ['marriage', 'divorce', 'hindu', 'matrimonial'],
            'ida': ['divorce', 'christian', 'marriage'],
            'iea': ['evidence', 'witness', 'proof', 'admissibility'],
            'nia': ['cheque', 'promissory note', 'bill of exchange', 'negotiable'],
            'mva': ['accident', 'vehicle', 'license', 'traffic'],
        }
        
        return keyword_mapping.get(act_key, [])
    
    def _load_indian_clause_types(self) -> Dict[str, Dict]:
        """
        Load clause types - could also be externalized later
        For now, keeping the India-specific ones as they're domain knowledge
        """
        # This is still valuable domain knowledge not easily found in datasets
        return {
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
            },
            'stamp_duty': {
                'description': 'Stamp duty and registration (India-specific)',
                'keywords': ['stamp duty', 'stamp paper', 'registration'],
                'risk_indicators': ['unstamped', 'insufficient stamp duty'],
                'indian_context': 'Mandatory under Indian Stamp Act; varies by state'
            },
            # Add other clause types...
        }
    
    def identify_applicable_acts(self, text: str) -> List[IndianAct]:
        """Identify which Indian Acts are applicable to the text"""
        text_lower = text.lower()
        applicable = []
        
        for act in self.acts.values():
            if any(keyword in text_lower for keyword in act.keywords):
                applicable.append(act)
        
        return applicable
    
    def search_sections(self, act_key: str, query: str) -> List[Dict]:
        """
        Search for sections within an act
        
        Args:
            act_key: Act identifier (e.g., 'ipc', 'crpc')
            query: Search term
        
        Returns:
            List of matching sections
        """
        if act_key not in self.acts:
            return []
        
        act = self.acts[act_key]
        query_lower = query.lower()
        
        matching_sections = []
        for section in act.sections:
            section_text = json.dumps(section).lower()
            if query_lower in section_text:
                matching_sections.append(section)
        
        return matching_sections


# Example usage
if __name__ == "__main__":
    print("🚀 Initializing Improved Indian Legal KB...\n")
    
    # Initialize with external data
    kb = ImprovedIndianLegalKB()
    
    print("\n" + "="*60)
    print("📚 Available Acts:")
    print("="*60)
    for act_key, act in kb.acts.items():
        print(f"  • {act.name} ({act.year}) - {len(act.sections)} sections")
    
    print("\n" + "="*60)
    print("🔍 Example: Search IPC for 'theft'")
    print("="*60)
    if 'ipc' in kb.acts:
        theft_sections = kb.search_sections('ipc', 'theft')
        for section in theft_sections[:3]:  # Show first 3
            print(f"  Section {section.get('section_no', 'N/A')}: {section.get('description', 'N/A')[:100]}...")
    
    print("\n" + "="*60)
    print("✅ Done! Ready to use real data instead of hardcoded KB!")
    print("="*60)
