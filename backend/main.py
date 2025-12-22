"""
FastAPI Server for Legal Document Analyzer - ENHANCED VERSION
Includes advanced clause extraction, risk analysis, and document comparison
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import shutil
from pathlib import Path
import uuid
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from document_processor import DocumentProcessor
# from ai_analyzer import LegalAIAnalyzer  # LEGACY: Only used for backwards compat
# from clause_extractor import ClauseExtractor  # DEPRECATED
# from risk_analyzer import RiskAnalyzer  # DEPRECATED: Pattern matching removed
from hybrid_analyzer import get_hybrid_analyzer  # Legal BERT + LLM
from ml_risk_scorer import get_ml_risk_scorer  # ML-based risk scoring

# Initialize FastAPI app
app = FastAPI(
    title="Legal Document Analyzer API - Enhanced",
    description="AI-powered legal document analysis with advanced clause extraction and risk assessment",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
document_processor = DocumentProcessor()
# REMOVED: Pattern matching components deprecated

# Pure ML/AI System
print("\n" + "="*60)
print("🚀 INITIALIZING PURE ML LEGAL ANALYZER")
print("   ✨ Legal BERT (NLP) + Groq LLM + Indian Legal KB")
print("   ❌ NO Pattern Matching - 100% Machine Learning")
print("="*60)
hybrid_analyzer = get_hybrid_analyzer()
ml_risk_scorer = get_ml_risk_scorer()
print("="*60 + "\n")

# Upload directory
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# In-memory storage (replace with database in production)
analysis_results = {}


class QuestionRequest(BaseModel):
    document_id: str
    question: str


class CompareRequest(BaseModel):
    document_id_1: str
    document_id_2: str


@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "online",
        "service": "Legal Document Analyzer API - Enhanced",
        "version": "2.0.0",
        "features": [
            "40+ clause types",
            "Advanced risk analysis",
            "Document comparison",
            "AI chatbot",
            "Risk heatmap"
        ]
    }


@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a legal document for analysis"""
    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Generate unique ID and save file
        document_id = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{document_id}{file_ext}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process document
        processed = document_processor.process_document(str(file_path))
        
        # Store metadata
        analysis_results[document_id] = {
            'id': document_id,
            'filename': file.filename,
            'file_path': str(file_path),
            'uploaded_at': datetime.now().isoformat(),
            'processed': processed,
            'status': 'uploaded'
        }
        
        return {
            'document_id': document_id,
            'filename': file.filename,
            'status': 'uploaded',
            'text_preview': processed['text'][:500],
            'metadata': processed['metadata']
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/{document_id}")
async def analyze_document(document_id: str):
    """
    Perform COMPLETE AI analysis with advanced features
    Returns: summary, clauses (40+ types), risk assessment, heatmap data
    """
    try:
        print(f"\n{'='*60}")
        print(f"📄 Analyzing document: {document_id}")
        print(f"{'='*60}\n")
        
        if document_id not in analysis_results:
            raise HTTPException(status_code=404, detail="Document not found")
        
        document_data = analysis_results[document_id]
        document_text = document_data['processed']['text']
        print(f"✅ Document loaded ({len(document_text)} chars)\n")
        
        
        # ========== NEW: HYBRID ANALYSIS (Legal BERT + LLM) ==========
        print("🔬 Running Hybrid Analysis (Legal BERT + Groq LLM)...")
        try:
            hybrid_results = hybrid_analyzer.analyze_complete(document_text)
            print("   ✅ Hybrid analysis complete\n")
            
            bert_extraction = hybrid_results['bert_extraction']
            indian_context = hybrid_results['indian_context']
            llm_analysis = hybrid_results['llm_analysis']
            summary = hybrid_results['summary']
            
        except Exception as e:
            print(f"   ❌ Hybrid Analysis FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
        
        
        # ========== ML-BASED RISK ANALYSIS (BERT + LLM) ==========
        print("🎯 Calculating ML-based risk score...")
        try:
            # Use BERT-classified clauses + LLM risk assessment
            ml_risk_analysis = ml_risk_scorer.calculate_ml_risk_score(
                clauses=bert_extraction['clauses'],  # Not ExtractedClause objects, need to convert
                llm_risk_assessment=llm_analysis['risk_assessment']
            )
            
            # Add missing clauses from Indian context
            ml_risk_analysis['missing_clauses'] = indian_context['missing_important_clauses']
            
            print(f"   ✅ ML Risk score: {ml_risk_analysis['overall_risk_score']}/100\n")
        except Exception as e:
            print(f"   ❌ ML Risk Analysis FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
        
        # Combine all analysis
        complete_analysis = {
            # AI Summary (from LLM)
            'ai_summary': {'summary': llm_analysis['detailed_analysis']},
            
            # Extracted clauses (from Legal BERT)
            'extracted_clauses': {
                'total_count': bert_extraction['total_count'],
                'by_category': bert_extraction['categorized'],
                'risk_summary': {
                    'High': sum(1 for c in bert_extraction['clauses'] if c['risk_level'] == 'High'),
                    'Medium': sum(1 for c in bert_extraction['clauses'] if c['risk_level'] == 'Medium'),
                    'Low': sum(1 for c in bert_extraction['clauses'] if c['risk_level'] == 'Low')
                },
                'method': 'Legal BERT NLP (No Pattern Matching)'
            },
            
            # Indian Legal Context (NEW)
            'indian_context': indian_context,
            
            # Entities (NEW - from Legal BERT)
            'entities': bert_extraction['entities'],
            
            # ML Risk Analysis (Pure ML - No Pattern Matching)
            'risk_analysis': ml_risk_analysis,
            
            # Executive Summary (NEW)
            'executive_summary': summary
        }
        
        # Update stored results
        print("💾 Saving analysis results...")
        analysis_results[document_id]['analysis'] = complete_analysis
        analysis_results[document_id]['status'] = 'analyzed'
        analysis_results[document_id]['analyzed_at'] = datetime.now().isoformat()
        
        print(f"\n{'='*60}")
        print(f"✅ Analysis Complete!")
        print(f"{'='*60}\n")
        
        return {
            'document_id': document_id,
            'status': 'analyzed',
            'analysis': complete_analysis
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/results/{document_id}")
async def get_results(document_id: str):
    """Retrieve analysis results for a document"""
    if document_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return analysis_results[document_id]


@app.post("/api/chat")
async def chat(request: QuestionRequest):
    """AI Q&A chatbot"""
    try:
        if request.document_id not in analysis_results:
            raise HTTPException(status_code=404, detail="Document not found")
        
        document_text = analysis_results[request.document_id]['processed']['text']
        
        # Get AI answer
        answer = ai_analyzer.answer_question(document_text, request.question)
        
        return {
            'document_id': request.document_id,
            'question': request.question,
            'answer': answer['answer']
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/compare")
async def compare_documents(request: CompareRequest):
    """Compare two legal documents"""
    try:
        if request.document_id_1 not in analysis_results:
            raise HTTPException(status_code=404, detail="Document 1 not found")
        if request.document_id_2 not in analysis_results:
            raise HTTPException(status_code=404, detail="Document 2 not found")
        
        doc1_text = analysis_results[request.document_id_1]['processed']['text']
        doc2_text = analysis_results[request.document_id_2]['processed']['text']
        doc1_name = analysis_results[request.document_id_1]['filename']
        doc2_name = analysis_results[request.document_id_2]['filename']
        
        # AI comparison
        ai_comparison = ai_analyzer.compare_documents(doc1_text, doc2_text)
        
        # Extract clauses from both
        clauses1 = clause_extractor.extract_clauses(doc1_text)
        clauses2 = clause_extractor.extract_clauses(doc2_text)
        
        # Compare risk scores
        risk1 = risk_analyzer.analyze_document_risk(doc1_text)
        risk2 = risk_analyzer.analyze_document_risk(doc2_text)
        
        return {
            'document_1': {
                'id': request.document_id_1,
                'name': doc1_name,
                'clause_count': len(clauses1),
                'risk_score': risk1['overall_risk_score'],
                'risk_level': risk1['risk_level']
            },
            'document_2': {
                'id': request.document_id_2,
                'name': doc2_name,
                'clause_count': len(clauses2),
                'risk_score': risk2['overall_risk_score'],
                'risk_level': risk2['risk_level']
            },
            'ai_comparison': ai_comparison,
            'score_difference': abs(risk1['overall_risk_score'] - risk2['overall_risk_score']),
            'recommendation': 'Document 1 is safer' if risk1['overall_risk_score'] < risk2['overall_risk_score'] else 'Document 2 is safer'
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/documents")
async def list_documents():
    """List all uploaded documents"""
    documents = [
        {
            'id': doc_id,
            'filename': data['filename'],
            'uploaded_at': data['uploaded_at'],
            'status': data['status'],
            'analyzed_at': data.get('analyzed_at', None)
        }
        for doc_id, data in analysis_results.items()
    ]
    return {'documents': documents, 'total': len(documents)}


@app.delete("/api/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document and its analysis"""
    if document_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file
    file_path = analysis_results[document_id]['file_path']
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Remove from memory
    del analysis_results[document_id]
    
    return {'status': 'deleted', 'document_id': document_id}


@app.get("/api/stats")
async def get_stats():
    """Get application statistics"""
    total_docs = len(analysis_results)
    analyzed_docs = sum(1 for d in analysis_results.values() if d['status'] == 'analyzed')
    
    return {
        'total_documents': total_docs,
        'analyzed_documents': analyzed_docs,
        'pending_documents': total_docs - analyzed_docs,
        'supported_formats': ['PDF', 'DOCX', 'TXT'],
        'clause_types_supported': 40,
        'ai_model': 'Google Gemini 1.5 Flash'
    }




@app.post("/api/compare/similarity/{document_id_1}/{document_id_2}")
async def compare_document_similarity(document_id_1: str, document_id_2: str):
    """
    Compare semantic similarity between two documents
    Returns similarity score and analysis
    """
    try:
        # Get both documents
        if document_id_1 not in analysis_results or document_id_2 not in analysis_results:
            raise HTTPException(status_code=404, detail="One or both documents not found")
        
        text1 = analysis_results[document_id_1]['processed']['text']
        text2 = analysis_results[document_id_2]['processed']['text']
        
        # Calculate similarity using InLegalBERT
        from legal_bert_analyzer import get_legal_bert_analyzer
        analyzer = get_legal_bert_analyzer()
        
        similarity_score = analyzer.calculate_similarity(text1, text2)
        
        # Get embeddings
        emb1 = analyzer.get_document_embedding(text1)
        emb2 = analyzer.get_document_embedding(text2)
        
        return {
            'document_1': {
                'id': document_id_1,
                'filename': analysis_results[document_id_1]['filename']
            },
            'document_2': {
                'id': document_id_2,
                'filename': analysis_results[document_id_2]['filename']
            },
            'similarity_score': float(similarity_score),
            'similarity_percentage': f"{similarity_score * 100:.1f}%",
            'interpretation': _interpret_similarity(similarity_score),
            'embeddings_available': bool(emb1 and emb2)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search/similar-clauses")
async def search_similar_clauses(
    document_id: str = Form(...),
    clause_text: str = Form(...)
):
    """
    Find clauses similar to the given text in a document
    """
    try:
        if document_id not in analysis_results:
            raise HTTPException(status_code=404, detail="Document not found")
        
        doc_data = analysis_results[document_id]
        
        # Get clauses from the correct location
        clauses = []
        if 'analysis' in doc_data:
            # New structure
            if 'bert_extraction' in doc_data['analysis']:
                clauses = doc_data['analysis']['bert_extraction'].get('clauses', [])
        elif 'clauses' in doc_data:
            # Fallback structure
            clauses = doc_data['clauses']
        
        if not clauses:
            return {
                'query': clause_text[:200],
                'document_id': document_id,
                'total_clauses': 0,
                'matches': [],
                'search_type': 'semantic',
                'error': 'No clauses found in document'
            }
        
        from legal_bert_analyzer import get_legal_bert_analyzer
        analyzer = get_legal_bert_analyzer()
        
        # Get embedding of search query
        query_embedding = analyzer.get_document_embedding(clause_text)
        
        # Compare with all clauses
        similarities = []
        
        for clause in clauses:
            # Handle both dict and object clauses
            clause_text_val = clause.get('text', '') if isinstance(clause, dict) else getattr(clause, 'text', '')
            clause_type = clause.get('type', 'unknown') if isinstance(clause, dict) else getattr(clause, 'type', 'unknown')
            
            if clause_text_val:
                try:
                    sim = analyzer.calculate_similarity(clause_text, clause_text_val)
                    if sim > 0:  # Only include non-zero similarities
                        similarities.append({
                            'clause': {
                                'text': clause_text_val,
                                'type': clause_type
                            },
                            'similarity': float(sim),
                            'similarity_percentage': f"{sim * 100:.1f}%"
                        })
                except Exception as e:
                    print(f"Error calculating similarity: {e}")
                    continue
        
        # Sort by similarity
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        return {
            'query': clause_text[:200],
            'document_id': document_id,
            'total_clauses': len(clauses),
            'matches': similarities[:10],  # Top 10 matches
            'search_type': 'semantic'
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Semantic search error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@app.get("/api/documents/classify/{document_id}")
async def classify_document(document_id: str):
    """
    Get AI-based document classification
    """
    try:
        if document_id not in analysis_results:
            raise HTTPException(status_code=404, detail="Document not found")
        
        text = analysis_results[document_id]['processed']['text']
        
        from legal_bert_analyzer import get_legal_bert_analyzer
        analyzer = get_legal_bert_analyzer()
        
        classification = analyzer.classify_document_type(text)
        
        # Get top classification
        top_type = max(classification, key=classification.get)
        
        return {
            'document_id': document_id,
            'filename': analysis_results[document_id]['filename'],
            'classification': classification,
            'top_type': top_type,
            'confidence': float(classification[top_type]),
            'method': 'InLegalBERT + Keywords'
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _interpret_similarity(score: float) -> str:
    """Interpret similarity score"""
    if score >= 0.9:
        return "Nearly identical"
    elif score >= 0.75:
        return "Very similar"
    elif score >= 0.6:
        return "Moderately similar"
    elif score >= 0.4:
        return "Somewhat similar"
    else:
        return "Different"


@app.post("/api/chat/ask")
async def chat_ask_question(request: dict):
    """
    AI chatbot endpoint - answers questions about the document
    """
    try:
        document_id = request.get('document_id')
        question = request.get('question')
        document_text = request.get('document_text', '')
        analysis_summary = request.get('analysis_summary', '')
        
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        # Get document from analysis results if available
        doc_context = ""
        if document_id and document_id in analysis_results:
            doc_data = analysis_results[document_id]
            if 'analysis' in doc_data:
                analysis = doc_data['analysis']
                doc_context = f"""
DOCUMENT ANALYSIS SUMMARY:
{analysis.get('ai_summary', {}).get('summary', '')}

RISK LEVEL: {analysis.get('risk_analysis', {}).get('risk_level', 'Unknown')}

APPLICABLE INDIAN ACTS:
{', '.join([act.get('name', '') for act in analysis.get('indian_context', {}).get('applicable_acts', [])])}

MISSING CLAUSES:
{', '.join([clause.get('clause_type', '') for clause in analysis.get('indian_context', {}).get('missing_important_clauses', [])])}
"""
        
        # Use AI analyzer for chatbot
        from ai_analyzer import LegalAIAnalyzer
        ai = LegalAIAnalyzer()
        
        prompt = f"""You are an expert legal assistant helping with Indian contract analysis.

DOCUMENT PREVIEW:
{document_text[:2000]}

{doc_context}

USER QUESTION: {question}

Provide a clear, specific answer based on the document and analysis. If referencing specific clauses or sections, mention them. Keep your answer concise but informative."""

        answer = ai._call_groq(prompt, max_tokens=500)
        
        return {
            'answer': answer,
            'question': question,
            'document_id': document_id
        }
    
    except Exception as e:
        print(f"Chatbot error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
