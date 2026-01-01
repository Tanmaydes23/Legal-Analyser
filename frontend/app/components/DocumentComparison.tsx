import React from 'react';

interface DocumentComparisonProps {
    documentId1: string;
    documentId2: string;
}

interface ComparisonResult {
    document_1: { id: string; filename: string };
    document_2: { id: string; filename: string };
    similarity_score: number;
    similarity_percentage: string;
    interpretation: string;
    embeddings_available: boolean;
}

export default function DocumentComparison({ documentId1, documentId2 }: DocumentComparisonProps) {
    const [comparison, setComparison] = React.useState<ComparisonResult | null>(null);
    const [loading, setLoading] = React.useState(false);

    React.useEffect(() => {
        if (documentId1 && documentId2) {
            compareDocuments();
        }
    }, [documentId1, documentId2]);

    const compareDocuments = async () => {
        setLoading(true);
        try {
            const response = await fetch(
                `http://localhost:8000/api/compare/similarity/${documentId1}/${documentId2}`,
                { method: 'POST' }
            );
            const data = await response.json();
            setComparison(data);
        } catch (error) {
            console.error('Comparison error:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="bg-white rounded-lg shadow-lg p-8">
                <div className="animate-pulse space-y-4">
                    <div className="h-6 bg-gray-200 rounded w-1/2 mx-auto"></div>
                    <div className="h-32 bg-gray-200 rounded"></div>
                </div>
            </div>
        );
    }

    if (!comparison) return null;

    const getColorForScore = (score: number) => {
        if (score >= 0.9) return 'from-green-500 to-emerald-600';
        if (score >= 0.75) return 'from-blue-500 to-cyan-600';
        if (score >= 0.6) return 'from-yellow-500 to-orange-500';
        if (score >= 0.4) return 'from-orange-500 to-red-500';
        return 'from-red-500 to-pink-600';
    };

    const getIconForScore = (score: number) => {
        if (score >= 0.9) return '🎯';
        if (score >= 0.75) return '✅';
        if (score >= 0.6) return '⚠️';
        return '❌';
    };

    return (
        <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl shadow-2xl p-8">
            <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">
                📊 Document Similarity Analysis
            </h2>

            {/* Documents Being Compared */}
            <div className="grid grid-cols-2 gap-4 mb-8">
                <div className="bg-white rounded-lg p-4 shadow">
                    <p className="text-sm text-gray-500 mb-1">Document 1</p>
                    <p className="font-semibold text-gray-800 truncate">
                        {comparison.document_1.filename}
                    </p>
                </div>
                <div className="bg-white rounded-lg p-4 shadow">
                    <p className="text-sm text-gray-500 mb-1">Document 2</p>
                    <p className="font-semibold text-gray-800 truncate">
                        {comparison.document_2.filename}
                    </p>
                </div>
            </div>

            {/* Similarity Score Visualization */}
            <div className="bg-white rounded-xl p-8 shadow-lg mb-6">
                <div className="text-center mb-6">
                    <div className="inline-flex items-center justify-center w-32 h-32 rounded-full bg-gradient-to-br from-purple-100 to-blue-100 mb-4">
                        <span className="text-5xl">{getIconForScore(comparison.similarity_score)}</span>
                    </div>
                    <h3 className="text-4xl font-bold bg-gradient-to-r ${getColorForScore(comparison.similarity_score)} bg-clip-text text-transparent mb-2">
                        {comparison.similarity_percentage}
                    </h3>
                    <p className="text-lg text-gray-600 font-medium">
                        {comparison.interpretation}
                    </p>
                </div>

                {/* Progress Bar */}
                <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                    <div
                        className={`bg-gradient-to-r ${getColorForScore(comparison.similarity_score)} h-4 rounded-full transition-all duration-1000 ease-out`}
                        style={{ width: `${comparison.similarity_score * 100}%` }}
                    />
                </div>

                {/* Score Details */}
                <div className="mt-6 grid grid-cols-3 gap-4 text-center">
                    <div>
                        <p className="text-2xl font-bold text-gray-800">
                            {(comparison.similarity_score * 100).toFixed(1)}
                        </p>
                        <p className="text-xs text-gray-500">Similarity Score</p>
                    </div>
                    <div>
                        <p className="text-2xl font-bold text-gray-800">
                            {comparison.embeddings_available ? '✓' : '✗'}
                        </p>
                        <p className="text-xs text-gray-500">Embeddings</p>
                    </div>
                    <div>
                        <p className="text-2xl font-bold text-gray-800">768</p>
                        <p className="text-xs text-gray-500">Dimensions</p>
                    </div>
                </div>
            </div>

            {/* Interpretation Guide */}
            <div className="bg-white rounded-lg p-4 text-sm">
                <p className="font-medium text-gray-700 mb-2">Understanding the Score:</p>
                <div className="space-y-1 text-gray-600">
                    <p>• <strong>90-100%:</strong> Nearly identical documents</p>
                    <p>• <strong>75-89%:</strong> Very similar structure and content</p>
                    <p>• <strong>60-74%:</strong> Moderately similar, same type</p>
                    <p>• <strong>40-59%:</strong> Somewhat similar clauses</p>
                    <p>• <strong>0-39%:</strong> Different documents</p>
                </div>
            </div>

            {/* Method Info */}
            <div className="mt-4 text-center">
                <p className="text-xs text-gray-500">
                    Powered by InLegalBERT Semantic Embeddings
                </p>
            </div>
        </div>
    );
}
