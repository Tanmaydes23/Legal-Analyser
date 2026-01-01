'use client';

import RiskBadge from './RiskBadge';

interface RiskHeatmapProps {
    data: {
        overall_score?: number;  // Legacy
        overall_risk_score?: number;  // New ML scorer
        risk_level: string;
        risk_matrix: {
            Critical: number;
            High: number;
            Medium: number;
            Low: number;
        };
        heatmap_data?: Array<{
            category: string;
            severities: any;
            total: number;
        }>;
    };
}

export default function RiskHeatmap({ data }: RiskHeatmapProps) {
    // Handle both old and new property names with proper defaults
    const riskScore = data.overall_risk_score ?? data.overall_score ?? 0;
    const matrix = data.risk_matrix || { Critical: 0, High: 0, Medium: 0, Low: 0 };
    const total = matrix.Critical + matrix.High + matrix.Medium + matrix.Low;

    const getPercentage = (count: number) => {
        if (total === 0) return 0;
        return (count / total) * 100;
    };

    return (
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Risk Overview</h2>
                <RiskBadge
                    level={data.risk_level as any}
                    score={riskScore}
                    size="lg"
                />
            </div>

            {/* Risk Score Gauge */}
            <div className="mb-6">
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                    <span>Risk Score</span>
                    <span className="font-bold">{riskScore.toFixed(1)}/100</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                    <div
                        className={`h-full rounded-full transition-all duration-500 ${data.overall_score >= 70 ? 'bg-gradient-to-r from-red-500 to-red-600' :
                            data.overall_score >= 50 ? 'bg-gradient-to-r from-orange-500 to-orange-600' :
                                data.overall_score >= 30 ? 'bg-gradient-to-r from-yellow-500 to-yellow-600' :
                                    'bg-gradient-to-r from-green-500 to-green-600'
                            }`}
                        style={{ width: `${data.overall_score}%` }}
                    />
                </div>
            </div>

            {/* Risk Matrix Grid */}
            <div className="space-y-3">
                <h3 className="text-sm font-semibold text-gray-700">Risk Breakdown</h3>

                {/* Critical */}
                {matrix.Critical > 0 && (
                    <div className="flex items-center space-x-3">
                        <div className="w-24 text-sm font-medium text-gray-700">Critical</div>
                        <div className="flex-1 bg-gray-100 rounded-full h-8 overflow-hidden">
                            <div
                                className="bg-gradient-to-r from-red-500 to-red-600 h-full flex items-center justify-end pr-3 text-white text-sm font-bold transition-all duration-500"
                                style={{ width: `${Math.max(15, getPercentage(matrix.Critical))}%` }}
                            >
                                {matrix.Critical}
                            </div>
                        </div>
                    </div>
                )}

                {/* High */}
                {matrix.High > 0 && (
                    <div className="flex items-center space-x-3">
                        <div className="w-24 text-sm font-medium text-gray-700">High</div>
                        <div className="flex-1 bg-gray-100 rounded-full h-8 overflow-hidden">
                            <div
                                className="bg-gradient-to-r from-orange-500 to-orange-600 h-full flex items-center justify-end pr-3 text-white text-sm font-bold transition-all duration-500"
                                style={{ width: `${Math.max(15, getPercentage(matrix.High))}%` }}
                            >
                                {matrix.High}
                            </div>
                        </div>
                    </div>
                )}

                {/* Medium */}
                {matrix.Medium > 0 && (
                    <div className="flex items-center space-x-3">
                        <div className="w-24 text-sm font-medium text-gray-700">Medium</div>
                        <div className="flex-1 bg-gray-100 rounded-full h-8 overflow-hidden">
                            <div
                                className="bg-gradient-to-r from-yellow-500 to-yellow-600 h-full flex items-center justify-end pr-3 text-white text-sm font-bold transition-all duration-500"
                                style={{ width: `${Math.max(15, getPercentage(matrix.Medium))}%` }}
                            >
                                {matrix.Medium}
                            </div>
                        </div>
                    </div>
                )}

                {/* Low */}
                {matrix.Low > 0 && (
                    <div className="flex items-center space-x-3">
                        <div className="w-24 text-sm font-medium text-gray-700">Low</div>
                        <div className="flex-1 bg-gray-100 rounded-full h-8 overflow-hidden">
                            <div
                                className="bg-gradient-to-r from-green-500 to-green-600 h-full flex items-center justify-end pr-3 text-white text-sm font-bold transition-all duration-500"
                                style={{ width: `${Math.max(15, getPercentage(matrix.Low))}%` }}
                            >
                                {matrix.Low}
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Total Count */}
            <div className="mt-4 pt-4 border-t">
                <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Total Risk Factors</span>
                    <span className="font-bold text-gray-900">{total}</span>
                </div>
            </div>
        </div>
    );
}
