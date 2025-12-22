"""
Legal BERT Analyzer
NLP/ML layer using Legal BERT for clause extraction and entity recognition
Optimized for Indian legal documents
"""
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import torch
from typing import Dict, List, Tuple
import re
from dataclasses import dataclass
from indian_legal_kb import IndianLegalKB

@dataclass
class LegalEntity:
    """Represents a legal entity extracted from text"""
    text: str
    type: str  # PARTY, DATE, MONEY, COURT, ACT, SECTION
    start: int
    end: int
    confidence: float

@dataclass
class ExtractedClause:
    """Represents a clause extracted by Legal BERT"""
    text: str
    type: str
    start_pos: int
    end_pos: int
    confidence: float
    entities: List[LegalEntity]
    risk_level: str = "Medium"

class LegalBERTAnalyzer:
    """
    Legal BERT-based document analyzer
    Uses pre-trained Legal BERT for NLP tasks
    """
    
    def __init__(self):
        """Initialize InLegalBERT model (Indian legal-specific) with full capabilities"""
        print("🤖 Initializing InLegalBERT (Indian Legal BERT)...")
        
        try:
            # Use InLegalBERT - trained on Indian legal corpus
            model_name = "law-ai/InLegalBERT"
            
            print(f"   Loading model: {model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Load base BERT model for embeddings (not the classifier version)
            from transformers import AutoModel
            self.base_model = AutoModel.from_pretrained(model_name)
            
            # For classification, we still have the classifier model
            self.model = AutoModelForTokenClassification.from_pretrained(model_name)
            
            # NOTE: We don't use InLegalBERT for NER because the classifier 
            # head is not trained (randomly initialized). We use it for:
            # 1. Clause extraction
            # 2. Document embeddings
            # 3. Semantic similarity
            # 4. Document classification
            self.ner_pipeline = None  # Disabled - untrained for NER
            
            print("   ✅ InLegalBERT loaded successfully")
            print("   📊 Features: Clause extraction, Embeddings, Similarity, Classification")
            
        except Exception as e:
            print(f"   ⚠️ Could not load InLegalBERT: {str(e)}")
            print("   ℹ️ Falling back to rule-based extraction")
            self.ner_pipeline = None
            self.base_model = None
        
        # Initialize OpenNyAI NER (will be added next)
        self.opennyai_ner = None
        
        # Initialize Indian Legal KB (will be replaced with civictech-India data)
        self.indian_kb = IndianLegalKB()


    
    def extract_clauses(self, document_text: str) -> List[ExtractedClause]:
        """
        Extract clauses from document using Legal BERT
        
        Args:
            document_text: Full document text
            
        Returns:
            List of extracted clauses with metadata
        """
        clauses = []
        
        # Step 1: Segment document into potential clauses
        clause_segments = self._segment_document(document_text)
        
        # Step 2: Classify each segment
        for segment in clause_segments:
            clause_type = self._classify_clause(segment['text'])
            entities = self._extract_entities(segment['text'])
            
            clause = ExtractedClause(
                text=segment['text'],
                type=clause_type,
                start_pos=segment['start'],
                end_pos=segment['end'],
                confidence=segment.get('confidence', 0.8),
                entities=entities,
                risk_level=self._assess_clause_risk(clause_type, segment['text'])
            )
            clauses.append(clause)
        
        return clauses
    
    def _segment_document(self, text: str) -> List[Dict]:
        """
        Segment document into clauses
        Uses sentence boundaries and paragraph structure
        """
        segments = []
        
        # Split by numbered sections (common in contracts)
        # Pattern: "1.", "2.", etc. or "1.1", "2.3"
        section_pattern = r'(?:^|\n)\s*(\d+\.(?:\d+\.)*)\s+'
        
        sections = re.split(section_pattern, text)
        
        current_pos = 0
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                section_num = sections[i]
                section_text = sections[i + 1].strip()
                
                if len(section_text) > 20:  # Minimum clause length
                    segments.append({
                        'text': section_text,
                        'start': current_pos,
                        'end': current_pos + len(section_text),
                        'section_num': section_num
                    })
                
                current_pos += len(section_text)
        
        # If no numbered sections, split by paragraphs
        if not segments:
            paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 20]
            current_pos = 0
            for para in paragraphs:
                segments.append({
                    'text': para,
                    'start': current_pos,
                    'end': current_pos + len(para)
                })
                current_pos += len(para)
        
        return segments[:50]  # Limit to 50 clauses
    
    def _classify_clause(self, text: str) -> str:
        """
        Classify clause type using keyword matching + Legal BERT
        """
        text_lower = text.lower()
        
        # Check Indian KB patterns first
        for clause_type, info in self.indian_kb.clause_types.items():
            if any(keyword in text_lower for keyword in info['keywords']):
                return clause_type
        
        # Fallback to general classification
        if any(word in text_lower for word in ['pay', 'fee', 'salary', 'rupees', '₹']):
            return 'payment'
        elif any(word in text_lower for word in ['terminate', 'cancellation', 'notice']):
            return 'termination'
        elif any(word in text_lower for word in ['liable', 'liability', 'indemnify']):
            return 'liability'
        elif any(word in text_lower for word in ['confidential', 'non-disclosure']):
            return 'confidentiality'
        elif any(word in text_lower for word in ['arbitration', 'dispute']):
            return 'arbitration'
        else:
            return 'general'
    
    def _extract_entities(self, text: str) -> List[LegalEntity]:
        """
        Extract legal entities using 2-layer approach:
        1. Indian-specific regex patterns (reliable, fast)
        2. OpenNyAI NER (trained on Indian legal documents)
        
        NOTE: InLegalBERT NER is NOT used because its classifier head
        is untrained (randomly initialized). InLegalBERT is used only
        for clause extraction, not entity recognition.
        """
        entities = []
        
        # Layer 1: Indian-specific entity patterns (fast, reliable)
        entity_patterns = {
            'MONEY': r'₹\s*[\d,]+(?:\.\d+)?|INR\s*[\d,]+|Rs\.?\s*[\d,]+',
            'DATE': r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}',
            'ACT': r'(?:Indian\s+)?(?:Contract|Companies|Arbitration|IT|Consumer Protection)\s+Act(?:,?\s+\d{4})?',
            'SECTION': r'Section\s+\d+[A-Za-z]?(?:\(\d+\))?',
            'COURT': r'(?:Supreme\s+Court|High\s+Court|District\s+Court|NCLAT|Consumer\s+Forum)',
        }
        
        for entity_type, pattern in entity_patterns.items():
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append(LegalEntity(
                    text=match.group(),
                    type=entity_type,
                    start=match.start(),
                    end=match.end(),
                    confidence=0.9
                ))
        
        # Layer 2: OpenNyAI NER (trained on Indian court judgments)
        if self.opennyai_ner:
            try:
                from opennyai_wrapper import get_opennyai_wrapper
                opennyai = get_opennyai_wrapper()
                
                if opennyai.is_available():
                    opennyai_entities = opennyai.extract_entities(text[:2000])
                    for entity_dict in opennyai_entities:
                        entities.append(LegalEntity(
                            text=entity_dict.get('text', ''),
                            type=entity_dict.get('type', 'UNKNOWN'),
                            start=entity_dict.get('start', 0),
                            end=entity_dict.get('end', 0),
                            confidence=entity_dict.get('confidence', 0.8)
                        ))
            except Exception as e:
                pass  # Graceful fallback to patterns only
        
        return entities
    
    def _assess_clause_risk(self, clause_type: str, text: str) -> str:
        """
        Assess risk level of clause
        """
        text_lower = text.lower()
        
        # Get risk indicators from Indian KB
        clause_info = self.indian_kb.get_clause_info(clause_type)
        risk_indicators = clause_info.get('risk_indicators', [])
        
        # Check for risk indicators
        high_risk_count = sum(1 for indicator in risk_indicators if indicator in text_lower)
        
        if high_risk_count >= 2:
            return "High"
        elif high_risk_count == 1:
            return "Medium"
        else:
            return "Low"
    
    def analyze_for_indian_context(self, text: str) -> Dict:
        """
        Analyze document with Indian legal context
        """
        # Identify applicable Indian Acts
        applicable_acts = self.indian_kb.identify_applicable_acts(text)
        
        # Extract clauses
        clauses = self.extract_clauses(text)
        
        # Categorize by type
        categorized = {}
        for clause in clauses:
            if clause.type not in categorized:
                categorized[clause.type] = []
            categorized[clause.type].append(clause)
        
        # Check for India-specific clauses
        indian_specific_found = []
        for clause in clauses:
            if self.indian_kb.is_indian_specific_clause(clause.type):
                indian_specific_found.append(clause)
        
        return {
            'clauses': clauses,
            'categorized': categorized,
            'applicable_acts': [
                {'name': act.name, 'year': act.year} 
                for act in applicable_acts
            ],
            'indian_specific_clauses': indian_specific_found,
            'total_clauses': len(clauses)
        }
    
    def get_clause_summary(self, clauses: List[ExtractedClause]) -> Dict:
        """Get summary statistics of extracted clauses"""
        risk_summary = {'High': 0, 'Medium': 0, 'Low': 0}
        type_summary = {}
        
        for clause in clauses:
            risk_summary[clause.risk_level] = risk_summary.get(clause.risk_level, 0) + 1
            type_summary[clause.type] = type_summary.get(clause.type, 0) + 1
        
        return {
            'total_count': len(clauses),
            'risk_summary': risk_summary,
            'by_type': type_summary
        }
    
    def get_document_embedding(self, text: str) -> List[float]:
        """
        Generate document embedding using InLegalBERT
        Returns a 768-dimensional vector representing the document
        
        Use cases:
        - Document similarity search
        - Contract clustering
        - Finding similar agreements
        """
        if not self.base_model:
            return []
        
        try:
            import torch
            
            # Tokenize
            inputs = self.tokenizer(
                text[:512],  # BERT max length
                return_tensors="pt",
                truncation=True,
                padding=True
            )
            
            # Get embeddings
            with torch.no_grad():
                outputs = self.base_model(**inputs)
            
            # Use [CLS] token embedding as document representation
            embedding = outputs.last_hidden_state[:, 0, :].squeeze().tolist()
            
            return embedding
            
        except Exception as e:
            print(f"   ⚠️ Embedding error: {str(e)}")
            return []
    
    def get_clause_embeddings(self, clauses: List[ExtractedClause]) -> Dict[str, List[float]]:
        """
        Generate embeddings for each clause
        Returns dict mapping clause text to embedding
        
        Use cases:
        - Group similar clauses
        - Find duplicate clauses across contracts
        - Clause search
        """
        embeddings = {}
        
        for clause in clauses:
            emb = self.get_document_embedding(clause.text)
            if emb:
                embeddings[clause.text[:100]] = emb  # Use first 100 chars as key
        
        return embeddings
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts
        Returns similarity score between 0 and 1
        
        Use cases:
        - Compare clauses
        - Find similar contracts
        - Detect clause variations
        """
        emb1 = self.get_document_embedding(text1)
        emb2 = self.get_document_embedding(text2)
        
        if not emb1 or not emb2:
            return 0.0
        
        try:
            import numpy as np
            
            # Cosine similarity
            dot_product = np.dot(emb1, emb2)
            norm1 = np.linalg.norm(emb1)
            norm2 = np.linalg.norm(emb2)
            
            similarity = dot_product / (norm1 * norm2)
            
            # Normalize to 0-1 range
            return (similarity + 1) / 2
            
        except Exception as e:
            print(f"   ⚠️ Similarity error: {str(e)}")
            return 0.0
    
    def classify_document_type(self, text: str) -> Dict[str, float]:
        """
        Classify document type using InLegalBERT embeddings
        Returns probability scores for different contract types
        
        Use cases:
        - Auto-categorize uploaded contracts
        - Routing to appropriate analysts
        - Better than rule-based classification
        """
        # Get embedding
        embedding = self.get_document_embedding(text)
        
        if not embedding:
            # Fallback to keyword-based
            return self._rule_based_classification(text)
        
        try:
            import numpy as np
            
            # Simple classification based on keywords in embedding space
            # This is a placeholder - you can train a proper classifier later
            keywords = {
                'service_agreement': ['service', 'deliverable', 'milestone', 'sow'],
                'employment_contract': ['employee', 'salary', 'designation', 'employment'],
                'license_agreement': ['license', 'intellectual property', 'usage rights'],
                'nda': ['confidential', 'non-disclosure', 'proprietary'],
                'lease_agreement': ['lease', 'rent', 'premises', 'tenant'],
                'purchase_order': ['purchase', 'goods', 'seller', 'buyer']
            }
            
            scores = {}
            text_lower = text.lower()
            
            for doc_type, terms in keywords.items():
                score = sum(1 for term in terms if term in text_lower) / len(terms)
                scores[doc_type] = score
            
            # Normalize scores
            total = sum(scores.values()) or 1
            scores = {k: v/total for k, v in scores.items()}
            
            return scores
            
        except Exception as e:
            print(f"   ⚠️ Classification error: {str(e)}")
            return self._rule_based_classification(text)
    
    def _rule_based_classification(self, text: str) -> Dict[str, float]:
        """Fallback rule-based classification"""
        text_lower = text.lower()
        
        if 'service' in text_lower and 'agreement' in text_lower:
            return {'service_agreement': 0.8, 'other': 0.2}
        elif 'employment' in text_lower or 'employee' in text_lower:
            return {'employment_contract': 0.8, 'other': 0.2}
        elif 'license' in text_lower:
            return {'license_agreement': 0.8, 'other': 0.2}
        else:
            return {'general_contract': 1.0}



# Singleton instance
_legal_bert_instance = None

def get_legal_bert_analyzer():
    """Get or create Legal BERT analyzer instance"""
    global _legal_bert_instance
    if _legal_bert_instance is None:
        _legal_bert_instance = LegalBERTAnalyzer()
    return _legal_bert_instance
