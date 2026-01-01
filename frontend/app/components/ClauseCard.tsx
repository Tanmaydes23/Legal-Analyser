'use client';

import { FileText, AlertCircle, CheckCircle, Info } from 'lucide-react';
import RiskBadge from './RiskBadge';

interface ClauseCardProps {
    clause: {
        type: string;
        text: string;
        risk_level: 'High' | 'Medium' | 'Low';
        location: string;
        explanation: string;
        recommendations: string[];
    };
}

export default function ClauseCard({ clause }: ClauseCardProps) {
    return (
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-5 hover:shadow-lg transition-shadow">
            {/* Header */}
            <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-2">
                    <FileText className="h-5 w-5 text-indigo-600" />
                    <h3 className="text-lg font-bold text-gray-900">{clause.type}</h3>
                </div>
                <RiskBadge level={clause.risk_level} size="sm" />
            </div>

            {/* Location */}
            <p className="text-xs text-gray-500 mb-3">{clause.location}</p>

            {/* Clause Text */}
            <div className="bg-gray-50 rounded-lg p-3 mb-3">
                <p className="text-sm text-gray-700 leading-relaxed line-clamp-4">{clause.text}</p>
            </div>

            {/* Explanation */}
            <div className="mb-3">
                <div className="flex items-center space-x-1 mb-1">
                    <Info className="h-4 w-4 text-blue-600" />
                    <span className="text-xs font-semibold text-gray-700">What this means:</span>
                </div>
                <p className="text-sm text-gray-600">{clause.explanation}</p>
            </div>

            {/* Recommendations */}
            {clause.recommendations && clause.recommendations.length > 0 && (
                <div className="border-t pt-3">
                    <div className="flex items-center space-x-1 mb-2">
                        <AlertCircle className="h-4 w-4 text-amber-600" />
                        <span className="text-xs font-semibold text-gray-700">Recommendations:</span>
                    </div>
                    <ul className="space-y-1">
                        {clause.recommendations.map((rec, idx) => (
                            <li key={idx} className="text-xs text-gray-600 flex items-start space-x-1">
                                <span className="text-amber-600 mt-0.5">•</span>
                                <span>{rec}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}
