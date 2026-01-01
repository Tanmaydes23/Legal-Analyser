import React from 'react';

interface SimilarClauseGroupsProps {
    groups: Array<{
        group_id: number;
        clause_count: number;
        clauses: string[];
        similarity: string;
    }>;
}

export default function SimilarClauseGroups({ groups }: SimilarClauseGroupsProps) {
    const [expandedGroup, setExpandedGroup] = React.useState<number | null>(null);

    const toggleGroup = (groupId: number) => {
        setExpandedGroup(expandedGroup === groupId ? null : groupId);
    };

    return (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-gray-800 flex items-center gap-2">
                    🔗 Similar Clause Groups
                    {groups && groups.length > 0 && (
                        <span className="text-xs font-normal bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                            {groups.length} groups found
                        </span>
                    )}
                </h3>
            </div>

            {!groups || groups.length === 0 ? (
                <div className="text-center py-8 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
                    <div className="text-4xl mb-3">✓</div>
                    <p className="text-gray-700 font-medium mb-2">No Similar Clauses Found</p>
                    <p className="text-sm text-gray-500">
                        All clauses in this document are unique. No duplicates or similar clauses detected.
                    </p>
                </div>
            ) : (
                <>
                    <p className="text-sm text-gray-600 mb-4">
                        These clauses have similar meaning and might be duplicates or variations:
                    </p>

                    <div className="space-y-3">
                        {groups.map((group) => (
                            <div
                                key={group.group_id}
                                className="border-2 border-yellow-200 rounded-lg overflow-hidden"
                            >
                                {/* Group Header */}
                                <button
                                    onClick={() => toggleGroup(group.group_id)}
                                    className="w-full flex items-center justify-between p-4 bg-yellow-50 hover:bg-yellow-100 transition-colors"
                                >
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-full bg-yellow-200 flex items-center justify-center font-bold text-yellow-800">
                                            {group.group_id + 1}
                                        </div>
                                        <div className="text-left">
                                            <p className="font-semibold text-gray-800">
                                                Group {group.group_id + 1}
                                            </p>
                                            <p className="text-sm text-gray-600">
                                                {group.clause_count} similar clauses
                                            </p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <span className="text-xs font-medium px-3 py-1 bg-yellow-200 text-yellow-800 rounded-full">
                                            {group.similarity} similarity
                                        </span>
                                        <svg
                                            className={`w-5 h-5 text-gray-600 transition-transform ${expandedGroup === group.group_id ? 'rotate-180' : ''
                                                }`}
                                            fill="none"
                                            stroke="currentColor"
                                            viewBox="0 0 24 24"
                                        >
                                            <path
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                strokeWidth={2}
                                                d="M19 9l-7 7-7-7"
                                            />
                                        </svg>
                                    </div>
                                </button>

                                {/* Group Content */}
                                {expandedGroup === group.group_id && (
                                    <div className="p-4 bg-white border-t-2 border-yellow-200">
                                        <div className="space-y-3">
                                            {group.clauses.map((clause, idx) => (
                                                <div
                                                    key={idx}
                                                    className="p-3 bg-gray-50 rounded-lg border-l-4 border-yellow-400"
                                                >
                                                    <div className="flex items-start gap-3">
                                                        <span className="flex-shrink-0 w-6 h-6 rounded-full bg-yellow-200 text-yellow-800 flex items-center justify-center text-xs font-bold">
                                                            {idx + 1}
                                                        </span>
                                                        <p className="text-sm text-gray-700 leading-relaxed flex-1">
                                                            {clause}
                                                        </p>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>

                                        {/* Warning/Recommendation */}
                                        <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                                            <p className="text-sm text-yellow-800 font-medium flex items-start gap-2">
                                                <span>⚠️</span>
                                                <span>
                                                    <strong>Recommendation:</strong> Review these clauses for consistency.
                                                    Similar clauses might indicate duplication or conflicting terms.
                                                </span>
                                            </p>
                                        </div>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </>
            )}

            {/* Info Footer */}
            <div className="mt-4 pt-4 border-t border-gray-200">
                <p className="text-xs text-gray-500 flex items-center gap-2">
                    <span className="inline-block w-2 h-2 bg-purple-500 rounded-full"></span>
                    Grouped using InLegalBERT embeddings and cosine similarity clustering
                </p>
            </div>
        </div>
    );
}
