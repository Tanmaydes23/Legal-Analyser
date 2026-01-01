'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Shield, Upload, FileText, CheckCircle, AlertTriangle, Info, TrendingUp, Scale, BookOpen, Sparkles } from 'lucide-react';

// Import the necessary components
import RiskBadge from '../components/RiskBadge';
import RiskHeatmap from '../components/RiskHeatmap';
import RiskFactorList from '../components/RiskFactorList';
import DocumentClassification from '../components/DocumentClassification';
import SemanticClauseSearch from '../components/SemanticClauseSearch';
import SimilarClauseGroups from '../components/SimilarClauseGroups';
import FloatingChatbot from '../components/FloatingChatbot';

export default function AnalyzePage() {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [analyzing, setAnalyzing] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [error, setError] = useState('');

    // NOTE: For a working application, replace this with your actual API endpoint
    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
            setError('');
        }
    };

    const handleUploadAndAnalyze = async () => {
        if (!file) {
            setError('Please select a file');
            return;
        }

        setUploading(true);
        setAnalyzing(true);
        setError('');

        try {
            const formData = new FormData();
            formData.append('file', file);

            const uploadRes = await fetch(`${API_URL}/api/upload`, {
                method: 'POST',
                body: formData,
            });

            if (!uploadRes.ok) throw new Error('Upload failed');
            const uploadData = await uploadRes.json();

            setUploading(false);

            const analyzeRes = await fetch(`${API_URL}/api/analyze/${uploadData.document_id}`, {
                method: 'POST',
            });

            if (!analyzeRes.ok) {
                const errorText = await analyzeRes.text();
                throw new Error(`Analysis failed: ${errorText}`);
            }
            const analyzeData = await analyzeRes.json();

            setResult(analyzeData);
            setAnalyzing(false);
        } catch (err: any) {
            setError(err.message || 'Something went wrong');
            setUploading(false);
            setAnalyzing(false);
        }
    };

    const getRiskColor = (level: string) => {
        const colors = {
            'Critical': 'from-red-500 to-red-600',
            'High': 'from-orange-500 to-orange-600',
            'Medium': 'from-yellow-500 to-yellow-600',
            'Low': 'from-green-500 to-green-600'
        };
        return colors[level as keyof typeof colors] || 'from-gray-500 to-gray-600';
    };

    const riskAnalysis = result?.analysis?.risk_analysis;
    const indianContext = result?.analysis?.indian_context;
    const documentIntelligence = result?.analysis?.document_intelligence;
    const documentId = result?.document_id;

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
            {/* Animated Background Mesh */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-30">
                <div className="absolute top-0 -left-4 w-[500px] h-[500px] bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl animate-blob"></div>
                <div className="absolute top-0 right-4 w-[500px] h-[500px] bg-indigo-500 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-2000"></div>
                <div className="absolute -bottom-8 left-20 w-[500px] h-[500px] bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-4000"></div>
            </div>

            {/* Header */}
            <header className="border-b border-white/10 bg-white/5 backdrop-blur-xl sticky top-0 z-50">
                <div className="w-full px-8 py-4">
                    <div className="flex justify-between items-center">
                        <Link href="/" className="flex items-center space-x-2">
                            <Shield className="h-7 w-7 text-indigo-400" />
                            <span className="text-xl font-bold text-white">Legal Analyzer</span>
                        </Link>
                        <Link href="/" className="text-sm text-gray-300 hover:text-white transition-colors">
                            ← Back to Home
                        </Link>
                    </div>
                </div>
            </header>

            {!result ? (
                // Upload Section
                <div className="w-full px-8 py-20 relative z-10">
                    <div className="max-w-5xl mx-auto">
                        <div className="text-center mb-16">
                            <h1 className="text-7xl font-bold bg-gradient-to-r from-white via-indigo-200 to-purple-200 bg-clip-text text-transparent mb-6 leading-tight">
                                Analyze Your Legal Document
                            </h1>
                            <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
                                Upload your contract, agreement, or any legal document to get instant AI analysis
                            </p>

                            {/* ML Badge */}
                            <div className="mt-8 inline-flex items-center space-x-2 bg-gradient-to-r from-indigo-500/20 to-purple-600/20 border border-indigo-400/30 px-6 py-3 rounded-full backdrop-blur-sm">
                                <Sparkles className="h-5 w-5 text-indigo-300" />
                                <span className="text-sm font-semibold text-indigo-200">100% Machine Learning • Legal BERT + Groq LLM</span>
                            </div>
                        </div>

                        {/* Upload Card */}
                        <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-16 text-center hover:bg-white/15 transition-all shadow-2xl">
                            <div className="flex flex-col items-center">
                                <div className="w-24 h-24 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center mb-6 shadow-2xl">
                                    <Upload className="h-12 w-12 text-white" />
                                </div>

                                <h3 className="text-3xl font-bold text-white mb-3">
                                    Upload Document
                                </h3>
                                <p className="text-gray-300 mb-8 text-lg">
                                    Supports PDF, DOCX, and TXT files (max 50MB)
                                </p>

                                <input
                                    type="file"
                                    accept=".pdf,.docx,.txt"
                                    onChange={handleFileChange}
                                    className="hidden"
                                    id="file-upload"
                                    disabled={uploading || analyzing}
                                />
                                <label
                                    htmlFor="file-upload"
                                    className="px-12 py-4 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-xl font-semibold text-lg cursor-pointer hover:shadow-2xl hover:shadow-purple-500/50 transform hover:-translate-y-1 transition-all"
                                >
                                    Choose File
                                </label>

                                {file && (
                                    <div className="mt-8 flex items-center space-x-3 text-base text-white bg-white/10 backdrop-blur-sm px-8 py-4 rounded-xl border border-white/20">
                                        <FileText className="h-6 w-6 text-indigo-300" />
                                        <span className="font-medium">{file.name}</span>
                                    </div>
                                )}
                            </div>
                        </div>

                        {file && (
                            <div className="mt-10 text-center">
                                <button
                                    onClick={handleUploadAndAnalyze}
                                    disabled={uploading || analyzing}
                                    className="px-16 py-5 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-2xl font-bold text-xl hover:shadow-2xl hover:shadow-purple-500/50 transform hover:-translate-y-1 hover:scale-105 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    {uploading ? 'Uploading...' : analyzing ? 'Analyzing with AI...' : 'Analyze Document'}
                                </button>
                            </div>
                        )}

                        {error && (
                            <div className="mt-8 p-6 bg-red-500/20 border border-red-500/50 rounded-2xl text-red-200 text-center backdrop-blur-sm">
                                {error}
                            </div>
                        )}

                        {/* Features Grid */}
                        <div className="mt-20 grid grid-cols-3 gap-8">
                            {[
                                { icon: Scale, title: 'Legal BERT', desc: 'ML-powered clause extraction', color: 'from-blue-500 to-cyan-500' },
                                { icon: BookOpen, title: 'Indian Law', desc: 'India-specific analysis', color: 'from-purple-500 to-pink-500' },
                                { icon: TrendingUp, title: '90%+ Accuracy', desc: 'Groq LLM powered', color: 'from-green-500 to-emerald-500' }
                            ].map((feature, i) => (
                                <div key={i} className="text-center bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6 hover:bg-white/10 transition-all">
                                    <div className={`w-14 h-14 bg-gradient-to-br ${feature.color} rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg`}>
                                        <feature.icon className="h-7 w-7 text-white" />
                                    </div>
                                    <h4 className="font-bold text-white mb-2 text-lg">{feature.title}</h4>
                                    <p className="text-sm text-gray-300">{feature.desc}</p>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* NEW: Advanced Features Section */}
                    <div className="max-w-7xl mx-auto mt-12 space-y-8">

                        {/* Section Header */}
                        <div className="text-center">
                            <h2 className="text-4xl font-bold text-white mb-3">
                                ✨ Advanced AI Features
                            </h2>
                            <p className="text-gray-300 text-lg">
                                Powered by InLegalBERT Embeddings & Semantic Analysis
                            </p>
                        </div>

                        {/* Document Classification */}
                        {documentId && (
                            <DocumentClassification documentId={documentId} />
                        )}

                        {/* Similar Clause Groups */}
                        {documentIntelligence?.similar_clause_groups && (
                            <SimilarClauseGroups
                                groups={documentIntelligence.similar_clause_groups}
                            />
                        )}

                        {/* Semantic Clause Search */}
                        {documentId && (
                            <SemanticClauseSearch documentId={documentId} />
                        )}

                    </div>
                </div>
            ) : (
                // Results Section - Full Dashboard View (Improved Layout)
                <div className="w-full px-8 py-12 relative z-10">
                    {/* Success Header */}
                    <div className="text-center mb-12">
                        <div className="inline-flex items-center justify-center w-20 h-20 bg-green-500/20 border border-green-500/50 rounded-full mb-4 backdrop-blur-sm">
                            <CheckCircle className="h-10 w-10 text-green-400" />
                        </div>
                        <h2 className="text-5xl font-bold text-white mb-3">Analysis Complete</h2>
                        <p className="text-gray-300 text-lg">Powered by Legal BERT + Groq LLM</p>

                        <button
                            onClick={() => { setResult(null); setFile(null); }}
                            className="mt-6 px-8 py-3 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white hover:bg-white/20 transition-all"
                        >
                            Analyze Another Document
                        </button>
                    </div>

                    {/* Risk Hero Card (Full Width) */}
                    {riskAnalysis && (
                        <div className={`max-w-7xl mx-auto bg-gradient-to-br ${getRiskColor(riskAnalysis.risk_level)} rounded-3xl p-10 text-white mb-10 shadow-2xl backdrop-blur-sm border border-white/20`}>
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-white/80 text-base font-medium mb-2">Overall Risk Level</p>
                                    <h3 className="text-6xl font-bold mb-3">{riskAnalysis.risk_level}</h3>
                                    <p className="text-3xl font-semibold">{(riskAnalysis.overall_risk_score || 0).toFixed(1)}/100</p>
                                </div>
                                <div className="text-right">
                                    <p className="text-base text-white/80 mb-2">Analysis Method</p>
                                    <p className="text-xl font-semibold">Legal BERT + Groq LLM</p>
                                    <p className="text-base text-white/80 mt-3">🇮🇳 Indian Law Aware</p>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Main Content: 2/3 (Summary + Risk Factors) and 1/3 (Heatmap + Context) */}
                    <div className="max-w-7xl mx-auto grid grid-cols-3 gap-8">

                        {/* 2/3 Column: Summary and Detailed Factors */}
                        <div className="col-span-2 space-y-6">

                            {/* AI Summary */}
                            <div className="bg-white rounded-3xl p-10 shadow-2xl border border-gray-200">
                                <h3 className="text-3xl font-bold text-gray-900 mb-6">AI Summary</h3>
                                <div className="prose max-w-none">
                                    <p className="text-gray-700 whitespace-pre-wrap leading-relaxed text-lg">
                                        {result.analysis?.ai_summary?.summary || 'No summary available'}
                                    </p>
                                </div>
                            </div>

                            {/* Detailed Risk Factors List */}
                            {riskAnalysis?.risk_factors && (
                                <div className="bg-white rounded-3xl p-10 shadow-2xl border border-gray-200">
                                    <h3 className="text-3xl font-bold text-gray-900 mb-6 flex items-center">
                                        <AlertTriangle className="h-8 w-8 text-orange-600 mr-3" />
                                        Detailed Risk Factors ({riskAnalysis.risk_factors.length})
                                    </h3>
                                    <RiskFactorList factors={riskAnalysis.risk_factors} />
                                </div>
                            )}
                        </div>

                        {/* 1/3 Column: Sidebar (Heatmap, Recommendations, Context) */}
                        <div className="space-y-6">

                            {/* Risk Heatmap / Matrix */}
                            {riskAnalysis && (
                                <RiskHeatmap
                                    data={riskAnalysis}
                                />
                            )}

                            {/* Recommendations */}
                            {riskAnalysis?.recommendations && (
                                <div className="bg-white rounded-3xl p-8 shadow-2xl border border-gray-200">
                                    <h3 className="text-2xl font-bold text-gray-900 mb-5 flex items-center">
                                        <Info className="h-6 w-6 text-blue-600 mr-3" />
                                        Key Recommendations
                                    </h3>
                                    <ul className="space-y-3">
                                        {riskAnalysis.recommendations.slice(0, 6).map((rec: string, i: number) => (
                                            <li key={i} className="flex items-start text-gray-700 text-base">
                                                <span className="text-blue-500 mr-2 mt-0.5">•</span>
                                                <span>{rec}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {/* Indian Context */}
                            {indianContext && (
                                <div className="bg-white rounded-3xl p-8 shadow-2xl border border-gray-200">
                                    <h3 className="text-2xl font-bold text-gray-900 mb-6">🇮🇳 Indian Legal Context</h3>
                                    <div className="space-y-4">
                                        <div>
                                            <p className="text-sm text-gray-500 mb-2">Document Type</p>
                                            <p className="font-semibold text-gray-900 text-lg">
                                                {indianContext.document_type?.replace('_', ' ').replace(/\b\w/g, (l: string) => l.toUpperCase()) || 'General Contract'}
                                            </p>
                                        </div>
                                        {indianContext.applicable_acts?.length > 0 && (
                                            <div>
                                                <p className="text-sm text-gray-500 mb-3">Applicable Acts</p>
                                                {indianContext.applicable_acts.slice(0, 4).map((act: any, i: number) => (
                                                    <div key={i} className="text-sm bg-indigo-50/50 border border-indigo-200 px-4 py-3 rounded-xl mb-3">
                                                        <span className="text-indigo-800 font-medium">{act.name}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}

                            {/* Missing Clauses */}
                            {indianContext?.missing_important_clauses?.length > 0 && (
                                <div className="bg-yellow-50 rounded-3xl p-8 shadow-2xl border border-yellow-300">
                                    <h3 className="text-2xl font-bold text-yellow-900 mb-5 flex items-center">
                                        <AlertTriangle className="h-6 w-6 text-yellow-600 mr-3" />
                                        Missing Clauses
                                    </h3>
                                    <ul className="space-y-3">
                                        {indianContext.missing_important_clauses.slice(0, 4).map((clause: any, i: number) => (
                                            <li key={i} className="text-base text-yellow-800">
                                                • {clause.clause_type?.replace('_', ' ')}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* NEW: Advanced Features Section - INSIDE results */}
                    <div className="max-w-7xl mx-auto mt-12 space-y-8 pb-12">

                        {/* Section Header */}
                        <div className="text-center">
                            <h2 className="text-4xl font-bold text-white mb-3">
                                ✨ Advanced AI Features
                            </h2>
                            <p className="text-gray-300 text-lg">
                                Powered by InLegalBERT Embeddings & Semantic Analysis
                            </p>
                        </div>

                        {/* Document Classification */}
                        {documentId && (
                            <DocumentClassification documentId={documentId} />
                        )}

                        {/* Similar Clause Groups */}
                        <SimilarClauseGroups
                            groups={documentIntelligence?.similar_clause_groups || []}
                        />

                        {/* Semantic Clause Search */}
                        {documentId && (
                            <SemanticClauseSearch documentId={documentId} />
                        )}

                    </div>
                </div>
            )}

            <style jsx global>{`
                @keyframes blob {
                    0%, 100% { transform: translate(0, 0) scale(1); }
                    33% { transform: translate(30px, -50px) scale(1.1); }
                    66% { transform: translate(-20px, 20px) scale(0.9); }
                }
                .animate-blob {
                    animation: blob 7s infinite;
                }
                .animation-delay-2000 {
                    animation-delay: 2s;
                }
                .animation-delay-4000 {
                    animation-delay: 4s;
                }
            `}</style>

            {/* Floating Chatbot - Shows only when results exist */}
            {result && (
                <FloatingChatbot
                    documentId={result.document_id || documentId || 'unknown'}
                    documentText={result.processed?.text || ''}
                    analysis={result.analysis || {}}
                />
            )}
        </div>
    );
}