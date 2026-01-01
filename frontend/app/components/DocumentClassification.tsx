import React from 'react';

interface DocumentClassificationProps {
    documentId: string;
}

interface ClassificationData {
    classification: Record<string, number>;
    top_type: string;
    confidence: number;
    method: string;
}

export default function DocumentClassification({ documentId }: DocumentClassificationProps) {
    const [classification, setClassification] = React.useState<ClassificationData | null>(null);
    const [loading, setLoading] = React.useState(false);

    React.useEffect(() => {
        if (documentId) {
            fetchClassification();
        }
    }, [documentId]);

    const fetchClassification = async () => {
        setLoading(true);
        try {
            const response = await fetch(
                `http://localhost:8000/api/documents/classify/${documentId}`
            );
            const data = await response.json();
            setClassification(data);
        } catch (error) {
            console.error('Classification error:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="bg-white rounded-lg shadow p-6">
                <div className="animate-pulse">
                    <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
                    <div className="h-8 bg-gray-200 rounded w-1/2"></div>
                </div>
            </div>
        );
    }

    if (!classification) return null;

    const getTypeLabel = (type: string) => {
        const labels: Record<string, string> = {
            service_agreement: 'Service Agreement',
            employment_contract: 'Employment Contract',
            license_agreement: 'License Agreement',
            nda: 'Non-Disclosure Agreement',
            lease_agreement: 'Lease Agreement',
            purchase_order: 'Purchase Order',
            general_contract: 'General Contract'
        };
        return labels[type] || type;
    };

    const getConfidenceColor = (confidence: number) => {
        if (confidence >= 0.8) return 'text-green-600 bg-green-50 border-green-200';
        if (confidence >= 0.6) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
        return 'text-orange-600 bg-orange-50 border-orange-200';
    };

    return (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-800">
                    📋 Document Classification
                </h3>
                <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                    {classification.method}
                </span>
            </div>

            {/* Primary Classification */}
            <div className={`border-2 rounded-lg p-4 mb-4 ${getConfidenceColor(classification.confidence)}`}>
                <div className="flex items-center justify-between">
                    <div>
                        <p className="text-sm font-medium opacity-75 mb-1">Identified as:</p>
                        <p className="text-2xl font-bold">
                            {getTypeLabel(classification.top_type)}
                        </p>
                    </div>
                    <div className="text-right">
                        <p className="text-sm font-medium opacity-75 mb-1">Confidence:</p>
                        <p className="text-3xl font-bold">
                            {(classification.confidence * 100).toFixed(0)}%
                        </p>
                    </div>
                </div>
            </div>

            {/* All Classifications */}
            <div className="space-y-2">
                <p className="text-sm font-medium text-gray-600 mb-3">
                    All Classifications:
                </p>
                {Object.entries(classification.classification)
                    .sort(([, a], [, b]) => b - a)
                    .map(([type, score]) => (
                        <div key={type} className="flex items-center gap-3">
                            <div className="flex-1">
                                <div className="flex justify-between mb-1">
                                    <span className="text-sm text-gray-700">
                                        {getTypeLabel(type)}
                                    </span>
                                    <span className="text-sm font-medium text-gray-900">
                                        {(score * 100).toFixed(1)}%
                                    </span>
                                </div>
                                <div className="w-full bg-gray-200 rounded-full h-2">
                                    <div
                                        className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-500"
                                        style={{ width: `${score * 100}%` }}
                                    />
                                </div>
                            </div>
                        </div>
                    ))}
            </div>

            {/* AI Badge */}
            <div className="mt-4 pt-4 border-t border-gray-200">
                <p className="text-xs text-gray-500 flex items-center gap-2">
                    <span className="inline-block w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                    AI-powered classification using InLegalBERT
                </p>
            </div>
        </div>
    );
}
