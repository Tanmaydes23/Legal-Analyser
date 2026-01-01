'use client';

import { AlertTriangle, TrendingUp, FileWarning } from 'lucide-react';

interface RiskFactorListProps {
    factors: Array<{
        category: string;
        severity: string;
        description: string;
        impact: string;
        mitigation: string;
        clause_reference: string;
    }>;
}

export default function RiskFactorList({ factors }: RiskFactorListProps) {
    if (!factors || factors.length === 0) {
        return (
            <div className="bg-green-50 rounded-xl border border-green-200 p-6 text-center">
                <TrendingUp className="h-12 w-12 text-green-600 mx-auto mb-3" />
                <p className="text-green-800 font-medium">No major risk factors detected!</p>
                <p className="text-green-600 text-sm mt-1">This document appears relatively safe</p>
            </div>
        );
    }

    const getSeverityColor = (severity: string) => {
        switch (severity) {
            case 'Critical':
                return 'bg-red-100 text-red-800 border-red-300';
            case 'High':
                return 'bg-orange-100 text-orange-800 border-orange-300';
            case 'Medium':
                return 'bg-yellow-100 text-yellow-800 border-yellow-300';
            default:
                return 'bg-blue-100 text-blue-800 border-blue-300';
        }
    };

    return (
        <div className="space-y-4">
            {factors.map((factor, idx) => (
                <div
                    key={idx}
                    className="bg-white rounded-xl shadow-md border border-gray-200 p-5 hover:shadow-lg transition-shadow"
                >
                    {/* Header */}
                    <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center space-x-2">
                            <AlertTriangle className="h-5 w-5 text-orange-600 flex-shrink-0" />
                            <h3 className="font-bold text-gray-900">{factor.category}</h3>
                        </div>
                        <div className={`px-2 py-1 rounded-md border text-xs font-semibold ${getSeverityColor(factor.severity)}`}>
                            {factor.severity}
                        </div>
                    </div>

                    {/* Description */}
                    <p className="text-sm text-gray-700 mb-3">{factor.description}</p>

                    {/* Impact */}
                    <div className="bg-red-50 rounded-lg p-3 mb-3">
                        <div className="flex items-start space-x-2">
                            <FileWarning className="h-4 w-4 text-red-600 mt-0.5 flex-shrink-0" />
                            <div>
                                <p className="text-xs font-semibold text-red-900 mb-1">Impact:</p>
                                <p className="text-sm text-red-800">{factor.impact}</p>
                            </div>
                        </div>
                    </div>

                    {/* Mitigation */}
                    <div className="bg-blue-50 rounded-lg p-3">
                        <p className="text-xs font-semibold text-blue-900 mb-1">💡 What to do:</p>
                        <p className="text-sm text-blue-800">{factor.mitigation}</p>
                    </div>

                    {/* Clause Reference */}
                    {factor.clause_reference && factor.clause_reference !== "Pattern not found" && (
                        <div className="mt-3 text-xs text-gray-500 italic border-l-2 border-gray-300 pl-3">
                            "{factor.clause_reference}"
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
}