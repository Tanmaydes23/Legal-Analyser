"""
OpenNyAI Alternative - Using spaCy Legal NER Model
Uses the pre-trained en_legal_ner_trf model from OpenNyAI on Hugging Face
"""
from typing import Dict, List, Optional
import os


class OpenNyAIWrapper:
    """
    Wrapper for OpenNyAI legal NER using their spaCy model from Hugging Face
    Model: https://huggingface.co/opennyaiorg/en_legal_ner_trf
    
    Trained on Indian court judgments with 14 entity types:
    COURT, PETITIONER, RESPONDENT, JUDGE, LAWYER, DATE, ORG, GPE,
    STATUTE, PROVISION, PRECEDENT, CASE_NUMBER, WITNESS, OTHER_PERSON
    """
    
    def __init__(self):
        """Initialize spaCy legal NER model"""
        print("🔍 Initializing OpenNyAI Legal NER (spaCy model)...")
        
        try:
            import spacy
            
            # Try to load from local directory first
            model_path = os.path.join(os.path.dirname(__file__), "en_legal_ner_trf")
            
            if os.path.exists(model_path):
                self.ner_model = spacy.load(model_path)
                self.available = True
                print("   ✅ OpenNyAI Legal NER loaded successfully (from local)")
            else:
                # Fallback: try loading if installed globally
                try:
                    self.ner_model = spacy.load("en_legal_ner_trf")
                    self.available = True
                    print("   ✅ OpenNyAI Legal NER loaded successfully")
                except:
                    print("   ⚠️ OpenNyAI Legal NER model not found")
                    print("   ℹ️ Clone from: https://huggingface.co/opennyaiorg/en_legal_ner_trf")
                    self.ner_model = None
                    self.available = False
            
        except ImportError:
            print("   ⚠️ spaCy not installed")
            self.ner_model = None
            self.available = False
            
        except Exception as e:
            print(f"   ⚠️ Could not load OpenNyAI Legal NER: {str(e)}")
            self.ner_model = None
            self.available = False
    
    def extract_entities(self, text: str) -> List[Dict]:
        """
        Extract legal entities using OpenNyAI's spaCy model
        
        Args:
            text: Legal document text
            
        Returns:
            List of entities with type, text, start, end, confidence
        """
        if not self.available or not self.ner_model:
            return []
        
        try:
            # Process text with spaCy NER
            doc = self.ner_model(text)
            
            # Convert to standard format
            entities = []
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'type': ent.label_,  # COURT, PETITIONER, JUDGE, etc.
                    'start': ent.start_char,
                    'end': ent.end_char,
                    'confidence': 0.9,  # spaCy doesn't provide scores for NER
                    'source': 'OpenNyAI-Legal-NER'
                })
            
            return entities
            
        except Exception as e:
            print(f"   ⚠️ OpenNyAI NER extraction error: {str(e)}")
            return []
    
    def is_available(self) -> bool:
        """Check if OpenNyAI Legal NER is available"""
        return self.available


# Singleton instance
_opennyai_instance = None

def get_opennyai_wrapper() -> OpenNyAIWrapper:
    """Get or create OpenNyAI wrapper instance"""
    global _opennyai_instance
    if _opennyai_instance is None:
        _opennyai_instance = OpenNyAIWrapper()
    return _opennyai_instance
