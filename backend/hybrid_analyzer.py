"""
Hybrid Legal Analyzer - NEW ARCHITECTURE
Combines InLegalBERT + OpenNyAI + CivicTech India + Heavy LLM
"""
from typing import Dict, List
from legal_bert_analyzer import get_legal_bert_analyzer, ExtractedClause
from ai_analyzer import LegalAIAnalyzer
from civictech_kb_loader import get_civictech_loader  # NEW: CivicTech data
# OpenNyAI removed - not needed (regex patterns handle entities)
from llm_risk_assessor import get_llm_risk_assessor  # NEW: LLM risk
from dataclasses import asdict

class HybridLegalAnalyzer:
    """
    NEW Hybrid analyzer combining:
    - InLegalBERT for clause extraction & entity recognition

    - CivicTech India for 8 Indian Acts data (from GitHub)
    - Groq LLM for intelligent risk assessment & recommendations
    """
    
    def __init__(self):
        """Initialize hybrid analyzer with new components"""
        print("🚀 Initializing NEW Hybrid Legal Analyzer...")
        print("   📦 InLegalBERT + CivicTech + Heavy LLM")
        
        # Layer 1: InLegalBERT (NLP/ML)
        self.bert_analyzer = get_legal_bert_analyzer()
        
        # Layer 2: CivicTech India KB (replaces hardcoded KB)
        self.civictech_loader = get_civictech_loader()
        self.indian_acts = self.civictech_loader.load_all_acts()
        
        # Layer 3: OpenNyAI - Removed (regex patterns sufficient for entity extraction)
        
        # Layer 4: LLM Risk Assessor (replaces rule-based risk)
        self.llm_assessor = get_llm_risk_assessor()
        
        # Layer 5: Groq LLM (for general analysis)
        self.llm = LegalAIAnalyzer()
        
        print("✅ NEW Hybrid analyzer ready!")
    
    def analyze_complete(self, document_text: str) -> Dict:
        """
        Complete hybrid analysis pipeline
        
        Args:
            document_text: Full document text
            
        Returns:
            Comprehensive analysis with BERT + LLM insights
        """
        print("\n🔍 Starting Hybrid Analysis...")
        
        # LAYER 1: Legal BERT Extraction
        print("  📊 Layer 1: Legal BERT extracting clauses...")
        bert_results = self.bert_analyzer.analyze_for_indian_context(document_text)
        clauses = bert_results['clauses']
        
        print(f"     ✅ Extracted {len(clauses)} clauses")
        
        # NEW: Generate document embedding and classification
        print("  🔬 Generating document embeddings and classification...")
        document_embedding = self.bert_analyzer.get_document_embedding(document_text)
        clause_embeddings = self.bert_analyzer.get_clause_embeddings(clauses)
        document_classification = self.bert_analyzer.classify_document_type(document_text)
        
        print(f"     ✅ Generated embeddings (768-dim)")
        print(f"     ✅ Document type: {max(document_classification, key=document_classification.get)}")
        
        # LAYER 2: Indian Legal Context
        print("  🇮🇳 Layer 2: Applying Indian legal context...")
        indian_context = self._enrich_with_indian_context(bert_results, document_text)
        
        # LAYER 3: LLM Enhancement
        print("  🤖 Layer 3: Groq LLM generating insights...")
        llm_analysis = self._generate_llm_analysis(
            document_text, 
            clauses, 
            indian_context
        )
        
        # NEW: Find similar clauses (group by similarity)
        similar_clause_groups = self._group_similar_clauses(clauses, clause_embeddings)
        
        # Combine results
        final_analysis = {
            'bert_extraction': {
                'clauses': self._format_clauses_for_output(clauses),
                'total_count': len(clauses),
                'categorized': self._categorize_clauses(clauses),
                'entities': self._extract_all_entities(clauses),
                'applicable_acts': bert_results['applicable_acts']
            },
            'document_intelligence': {  # NEW
                'embedding': document_embedding[:10],  # First 10 dims for preview
                'classification': document_classification,
                'similar_clause_groups': similar_clause_groups,
                'embedding_dimensions': 768
            },
            'indian_context': indian_context,
            'llm_analysis': llm_analysis,
            'summary': self._generate_executive_summary(
                bert_results, indian_context, llm_analysis
            )
        }
        
        print("  ✅ Hybrid analysis complete!\\n")
        
        return final_analysis

    
    
    def _enrich_with_indian_context(self, bert_results: Dict, text: str) -> Dict:
        """Add Indian legal context using CivicTech data and LLM"""
        
        # Identify applicable Indian Acts from CivicTech data
        applicable_acts = self.civictech_loader.identify_applicable_acts(
            text, 
            self.indian_acts
        )
        
        # Check for India-specific clauses
        indian_clauses = bert_results.get('indian_specific_clauses', [])
        
        # Determine document type (can enhance this with LLM later)
        document_type = self._determine_document_type(bert_results['clauses'])
        
        # Use LLM to detect missing clauses (replaces hardcoded checklist)
        missing_analysis = self.llm_assessor.detect_missing_clauses(
            found_clauses=self._format_clauses_for_output(bert_results['clauses']),
            document_type=document_type,
            applicable_acts=[{
                'name': act.name,
                'year': act.year,
                'type': act.act_type
            } for act in applicable_acts],
            document_text=text
        )
        
        return {
            'document_type': document_type,
            'applicable_acts': [
                {
                    'name': act.name,
                    'year': act.year,
                    'short_name': act.short_name,
                    'type': act.act_type,
                    'source': 'CivicTech India',
                    'relevance': 'High'
                } for act in applicable_acts
            ],
            'india_specific_clauses': [
                {
                    'type': clause.type,
                    'text': clause.text[:200] + '...',
                    'importance': 'Mandatory in India'
                } for clause in indian_clauses
            ],
            'missing_important_clauses': missing_analysis.get('missing_clauses', []),
            'compliance_score': missing_analysis.get('compliance_score', 50),
            'critical_gaps': missing_analysis.get('critical_gaps', []),
            'detection_method': 'LLM-based (Groq)',
            'jurisdiction': 'India'
        }
    
    def _generate_llm_analysis(self, document_text: str, clauses: List, 
                               indian_context: Dict) -> Dict:
        """
        Generate LLM analysis with Indian legal context
        Uses India-aware prompts
        """
        
        # Prepare context for LLM
        clauses_summary = self._format_clauses_for_llm(clauses[:10])  # Top 10
        acts_summary = ', '.join([act['name'] for act in indian_context['applicable_acts']])
        
        # India-specific prompt
        prompt = f"""You are an expert in Indian contract law. Analyze this legal document carefully.

DOCUMENT TYPE: {indian_context['document_type']}

APPLICABLE INDIAN LAWS: {acts_summary}

KEY CLAUSES FOUND:
{clauses_summary}

INDIA-SPECIFIC CONSIDERATIONS:
- This is governed by Indian law
- Consider Indian Contract Act, 1872
- Consider relevant Supreme Court precedents
- Consider compliance requirements in India

Please provide:
1. Executive Summary (2-3 sentences)
2. Key Strengths of this contract
3. Key Weaknesses or Risks (specific to Indian law)
4. Recommendations for improvement
5. Any red flags under Indian law

Focus on practical implications for Indian businesses/individuals.
"""
        
        # Call Groq LLM
        llm_response = self.llm._call_groq(prompt, max_tokens=2000)
        
        # Also get risk assessment
        risk_prompt = f"""Assess the legal risks in this Indian contract:

{document_text[:3000]}

Consider:
- Indian Contract Act, 1872
- Specific Relief Act, 1963
- Recent Indian court rulings
- Enforceability in Indian courts

Rate overall risk: Low, Medium, High, or Critical
List top 3 risk factors.
"""
        
        risk_assessment = self.llm._call_groq(risk_prompt, max_tokens=1000)
        
        return {
            'detailed_analysis': llm_response,
            'risk_assessment': risk_assessment,
            'indian_law_compliance': self._check_indian_compliance(clauses)
        }
    
    def _format_clauses_for_llm(self, clauses: List[ExtractedClause]) -> str:
        """Format clauses for LLM prompt"""
        formatted = []
        for i, clause in enumerate(clauses, 1):
            formatted.append(
                f"{i}. {clause.type.upper()}: {clause.text[:150]}..."
            )
        return '\n'.join(formatted)
    
    def _format_clauses_for_output(self, clauses: List[ExtractedClause]) -> List[Dict]:
        """Format clauses for API response"""
        return [
            {
                'text': clause.text,
                'type': clause.type,
                'risk_level': clause.risk_level,
                'confidence': round(clause.confidence, 2),
                'entities': [
                    {
                        'text': e.text,
                        'type': e.type,
                        'confidence': round(e.confidence, 2)
                    } for e in clause.entities
                ],
                'location': f"Position {clause.start_pos}-{clause.end_pos}"
            }
            for clause in clauses
        ]
    
    def _categorize_clauses(self, clauses: List[ExtractedClause]) -> Dict:
        """Categorize clauses by type"""
        categorized = {}
        for clause in clauses:
            if clause.type not in categorized:
                categorized[clause.type] = []
            categorized[clause.type].append({
                'text': clause.text[:200] + ('...' if len(clause.text) > 200 else ''),
                'risk_level': clause.risk_level
            })
        return categorized
    
    def _extract_all_entities(self, clauses: List[ExtractedClause]) -> Dict:
        """Extract all unique entities"""
        entities_by_type = {}
        
        for clause in clauses:
            for entity in clause.entities:
                if entity.type not in entities_by_type:
                    entities_by_type[entity.type] = set()
                entities_by_type[entity.type].add(entity.text)
        
        # Convert sets to lists
        return {
            etype: list(values) 
            for etype, values in entities_by_type.items()
        }
    
    def _determine_document_type(self, clauses: List[ExtractedClause]) -> str:
        """Determine document type from clauses"""
        clause_types = [c.type for c in clauses]
        
        if 'tds_clause' in clause_types or clause_types.count('payment') > 2:
            return 'service_agreement'
        elif 'employment' in ' '.join(clause_types) or clause_types.count('termination') > 1:
            return 'employment_contract'
        elif 'intellectual_property' in clause_types:
            return 'license_agreement'
        else:
            return 'general_contract'
    
    def _identify_missing_clauses(self, clauses: List[ExtractedClause], 
                                  document_type: str) -> List[Dict]:
        """
        Identify missing clauses using LLM (called by _enrich_with_indian_context)
        NOTE: This is now handled by LLM assessor in _enrich_with_indian_context
        Keeping as fallback only
        """
        # Fallback logic - should not be called in new architecture
        return []
    
    def _check_indian_compliance(self, clauses: List[ExtractedClause]) -> Dict:
        """
        Check Indian compliance using LLM assessor (replaces hardcoded rules)
        """
        # Use LLM-based compliance checking
        try:
            compliance_result = self.llm_assessor.check_indian_compliance(
                document_text="",  # Can pass full text if available
                clauses=self._format_clauses_for_output(clauses),
                applicable_acts=[{
                    'name': act.name,
                    'year': act.year
                } for act in self.indian_acts.values()]
            )
            return compliance_result
        except Exception as e:
            print(f"   ⚠️ LLM compliance check error: {str(e)}")
            # Fallback
            return {
                'compliance_score': 50,
                'compliance_checks': {},
                'compliance_issues': ['Could not complete LLM compliance check'],
                'method': 'Fallback'
            }
    
    
    def _group_similar_clauses(self, clauses: List, clause_embeddings: Dict) -> List[Dict]:
        """Group similar clauses together using embeddings"""
        if not clause_embeddings:
            return []
        
        try:
            import numpy as np
            from sklearn.cluster import AgglomerativeClustering
            
            # Convert embeddings to matrix
            texts = list(clause_embeddings.keys())
            embeddings_matrix = np.array(list(clause_embeddings.values()))
            
            if len(embeddings_matrix) < 2:
                return []
            
            # Cluster similar clauses
            clustering = AgglomerativeClustering(
                n_clusters=min(5, len(embeddings_matrix)),
                metric='cosine',
                linkage='average'
            )
            labels = clustering.fit_predict(embeddings_matrix)
            
            # Group by cluster
            groups = {}
            for idx, label in enumerate(labels):
                if label not in groups:
                    groups[label] = []
                groups[label].append(texts[idx])
            
            # Format output
            result = []
            for group_id, clause_list in groups.items():
                if len(clause_list) > 1:  # Only groups with multiple clauses
                    result.append({
                        'group_id': int(group_id),
                        'clause_count': len(clause_list),
                        'clauses': clause_list,
                        'similarity': 'high'
                    })
            
            return result
            
        except Exception as e:
            print(f"   ⚠️ Clause grouping error: {str(e)}")
            return []
    
    def _generate_executive_summary(self, bert_results: Dict, 
                                   indian_context: Dict, llm_analysis: Dict) -> Dict:
        """Generate executive summary"""
        # bert_results is actually the full hybrid results with 'bert_extraction' key
        bert_extraction = bert_results.get('bert_extraction', bert_results)
        total_clauses = bert_extraction.get('total_count', 0)
        document_type = indian_context['document_type']
        applicable_acts = len(indian_context['applicable_acts'])
        
        return {
            'document_type': document_type.replace('_', ' ').title(),
            'total_clauses_analyzed': total_clauses,
            'indian_laws_applicable': applicable_acts,
            'analysis_method': 'Legal BERT + Groq LLM (India-optimized)',
            'confidence': 'High',
            'jurisdiction': 'India'
        }


# Singleton
_hybrid_instance = None

def get_hybrid_analyzer():
    """Get or create hybrid analyzer instance"""
    global _hybrid_instance
    if _hybrid_instance is None:
        _hybrid_instance = HybridLegalAnalyzer()
    return _hybrid_instance
