"""
CivicTech India Knowledge Base Loader
Loads Indian legal acts from civictech-India GitHub repository
Replaces hardcoded Indian Legal KB with community-maintained JSON data
"""
import requests
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
import os

@dataclass
class IndianAct:
    """Represents an Indian legal act from civictech-India"""
    name: str
    year: int
    short_name: str
    sections: List[Dict]
    keywords: List[str]
    act_type: str  # criminal, civil, tax, etc.


class CivicTechKBLoader:
    """
    Loads Indian legal data from civictech-India GitHub repository
    Source: https://github.com/civictech-India/Indian-Law-Penal-Code-Json
    """
    
    def __init__(self, cache_dir: str = "./legal_data_cache"):
        """Initialize with optional caching"""
        self.cache_dir = cache_dir
        self.github_base = "https://raw.githubusercontent.com/civictech-India/Indian-Law-Penal-Code-Json/master"
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
        
        # Act configurations
        self.acts_config = {
            'ipc': {
                'file': 'ipc.json',
                'name': 'Indian Penal Code',
                'year': 1860,
                'type': 'criminal',
                'keywords': ['murder', 'theft', 'assault', 'criminal', 'offence', 'punishment', 'cheating', 'fraud']
            },
            'crpc': {
                'file': 'crpc.json',
                'name': 'Code of Criminal Procedure',
                'year': 1973,
                'type': 'criminal',
                'keywords': ['arrest', 'bail', 'trial', 'procedure', 'investigation', 'cognizable', 'warrant']
            },
            'cpc': {
                'file': 'cpc.json',
                'name': 'Civil Procedure Code',
                'year': 1908,
                'type': 'civil',
                'keywords': ['suit', 'decree', 'civil', 'plaintiff', 'defendant', 'judgment', 'appeal']
            },
            'hma': {
                'file': 'hma.json',
                'name': 'Hindu Marriage Act',
                'year': 1955,
                'type': 'civil',
                'keywords': ['marriage', 'divorce', 'hindu', 'matrimonial', 'restitution', 'conjugal']
            },
            'ida': {
                'file': 'ida.json',
                'name': 'Indian Divorce Act',
                'year': 1869,
                'type': 'civil',
                'keywords': ['divorce', 'christian', 'marriage', 'separation', 'matrimonial']
            },
            'iea': {
                'file': 'iea.json',
                'name': 'Indian Evidence Act',
                'year': 1872,
                'type': 'procedural',
                'keywords': ['evidence', 'witness', 'proof', 'admissibility', 'testimony', 'cross-examination']
            },
            'nia': {
                'file': 'nia.json',
                'name': 'Negotiable Instruments Act',
                'year': 1881,
                'type': 'commercial',
                'keywords': ['cheque', 'promissory note', 'bill of exchange', 'negotiable', 'dishonour', 'bounce']
            },
            'mva': {
                'file': 'mva.json',
                'name': 'Motor Vehicles Act',
                'year': 1988,
                'type': 'regulatory',
                'keywords': ['accident', 'vehicle', 'license', 'traffic', 'motor', 'driving', 'insurance']
            }
        }
    
    def load_all_acts(self, use_cache: bool = True) -> Dict[str, IndianAct]:
        """
        Load all available Indian acts from civictech-India
        
        Args:
            use_cache: Use cached files if available
            
        Returns:
            Dictionary of act_key -> IndianAct objects
        """
        print("📚 Loading Indian Acts from civictech-India...")
        acts = {}
        
        for act_key, config in self.acts_config.items():
            try:
                act_data = self._load_act(act_key, config, use_cache)
                if act_data:
                    acts[act_key] = act_data
                    print(f"   ✅ {config['name']} ({config['year']}) - {len(act_data.sections)} sections")
            except Exception as e:
                print(f"   ⚠️ Failed to load {act_key}: {str(e)}")
                continue
        
        print(f"✅ Loaded {len(acts)} acts from civictech-India\n")
        return acts
    
    def _load_act(self, act_key: str, config: Dict, use_cache: bool) -> Optional[IndianAct]:
        """Load a single act from GitHub or cache"""
        cache_file = os.path.join(self.cache_dir, config['file'])
        
        # Try cache first
        if use_cache and os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            # Download from GitHub
            url = f"{self.github_base}/{config['file']}"
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            
            # Cache the data
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Extract sections from JSON
        sections = self._extract_sections(data)
        
        return IndianAct(
            name=config['name'],
            year=config['year'],
            short_name=f"{act_key.upper()} {config['year']}",
            sections=sections,
            keywords=config['keywords'],
            act_type=config['type']
        )
    
    def _extract_sections(self, data) -> List[Dict]:
        """
        Extract sections from civictech-India JSON format
        
        The civictech-India JSONs are direct arrays of sections:
        [{"Section": 1, "section_title": "...", ...}, {...}, ...]
        """
        sections = []
        
        # If data is already a list (civictech-India format)
        if isinstance(data, list):
            return data  # Already a list of sections!
        
        # Fallback: handle dict formats (if any exist)
        if isinstance(data, dict):
            # Direct sections array
            if 'sections' in data:
                sections = data['sections']
            
            # Chapters containing sections
            elif 'chapters' in data:
                for chapter in data['chapters']:
                    if 'sections' in chapter:
                        sections.extend(chapter['sections'])
            
            # Parts containing sections
            elif 'parts' in data:
                for part in data['parts']:
                    if 'sections' in part:
                        sections.extend(part['sections'])
        
        return sections
    
    def identify_applicable_acts(self, text: str, acts: Dict[str, IndianAct]) -> List[IndianAct]:
        """Identify which acts are applicable to given text"""
        text_lower = text.lower()
        applicable = []
        
        for act in acts.values():
            if any(keyword in text_lower for keyword in act.keywords):
                applicable.append(act)
        
        return applicable
    
    def search_sections(self, act_key: str, query: str, acts: Dict[str, IndianAct]) -> List[Dict]:
        """Search for sections within an act"""
        if act_key not in acts:
            return []
        
        act = acts[act_key]
        query_lower = query.lower()
        
        matching_sections = []
        for section in act.sections:
            section_text = json.dumps(section).lower()
            if query_lower in section_text:
                matching_sections.append(section)
        
        return matching_sections


# Singleton instance
_civictech_loader = None

def get_civictech_loader() -> CivicTechKBLoader:
    """Get or create CivicTech KB loader instance"""
    global _civictech_loader
    if _civictech_loader is None:
        _civictech_loader = CivicTechKBLoader()
    return _civictech_loader
