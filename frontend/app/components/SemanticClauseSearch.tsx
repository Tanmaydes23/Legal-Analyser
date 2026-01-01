import React from 'react';

interface SemanticClauseSearchProps {
    documentId: string;
}

interface ClauseMatch {
    clause: {
        text: string;
        type: string;
        risk_level?: string;
    };
    similarity: number;
    similarity_percentage: string;
}

interface SearchResult {
    query: string;
    document_id: string;
    total_clauses: number;
    matches: ClauseMatch[];
    search_type: string;
}

export default function SemanticClauseSearch({ documentId }: SemanticClauseSearchProps) {
    const [searchQuery, setSearchQuery] = React.useState('');
    const [results, setResults] = React.useState<SearchResult | null>(null);
    const [loading, setLoading] = React.useState(false);

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!searchQuery.trim()) return;

        setLoading(true);
        try {
            const formData = new FormData();
            formData.append('document_id', documentId);
            formData.append('clause_text', searchQuery);

            const response = await fetch('http://localhost:8000/api/search/similar-clauses', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            setResults(data);
        } catch (error) {
            console.error('Search error:', error);
        } finally {
            setLoading(false);
        }
    };

    const getSimilarityColor = (sim: number) => {
        if (sim >= 0.9) return 'bg-green-100 border-green-400 text-green-800';
        if (sim >= 0.75) return 'bg-blue-100 border-blue-400 text-blue-800';
        if (sim >= 0.6) return 'bg-yellow-100 border-yellow-400 text-yellow-800';
        return 'bg-gray-100 border-gray-400 text-gray-800';
    };

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                🔍 Semantic Clause Search
                <span className="text-xs font-normal text-gray-500 bg-purple-100 px-2 py-1 rounded">
                    AI-Powered
                </span>
            </h3>

            {/* Search Form */}
            <form onSubmit={handleSearch} className="mb-6">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="Search by meaning... e.g., 'payment within 30 days'"
                        className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-purple-500 focus:outline-none transition-colors"
                    />
                    <button
                        type="submit"
                        disabled={loading || !searchQuery.trim()}
                        className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-lg hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                    >
                        {loading ? 'Searching...' : 'Search'}
                    </button>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                    💡 Tip: Search finds clauses by <strong>meaning</strong>, not just keywords!
                </p>
            </form>

            {/* Loading State */}
            {loading && (
                <div className="space-y-3">
                    {[1, 2, 3].map(i => (
                        <div key={i} className="animate-pulse">
                            <div className="h-24 bg-gray-200 rounded-lg"></div>
                        </div>
                    ))}
                </div>
            )}

            {/* Results */}
            {results && !loading && (
                <div>
                    <div className="flex items-center justify-between mb-4 p-3 bg-gray-50 rounded-lg">
                        <p className="text-sm text-gray-600">
                            Searched in <strong>{results.total_clauses || 0}</strong> clauses
                        </p>
                        <p className="text-sm font-medium text-purple-600">
                            Found {results.matches?.length || 0} matches
                        </p>
                    </div>

                    {(!results.matches || results.matches.length === 0) ? (
                        <div className="text-center py-8">
                            <p className="text-gray-500">No similar clauses found</p>
                            <p className="text-sm text-gray-400 mt-2">
                                Try rephrasing your search query
                            </p>
                        </div>
                    ) : (
                        <div className="space-y-3">
                            {results.matches?.map((match, idx) => (
                                <div
                                    key={idx}
                                    className={`border-l-4 rounded-lg p-4 transition-all hover:shadow-md ${getSimilarityColor(match.similarity)}`}
                                >
                                    <div className="flex items-start justify-between mb-2">
                                        <span className="text-xs font-semibold uppercase tracking-wide">
                                            {match.clause?.type?.replace('_', ' ') || 'Unknown'}
                                        </span>
                                        <div className="flex items-center gap-2">
                                            <span className="text-lg font-bold">
                                                {match.similarity_percentage}
                                            </span>
                                            <div className="w-16 bg-white rounded-full h-2">
                                                <div
                                                    className="bg-current h-2 rounded-full"
                                                    style={{ width: `${match.similarity * 100}%` }}
                                                />
                                            </div>
                                        </div>
                                    </div>
                                    <p className="text-sm text-gray-700 leading-relaxed">
                                        {match.clause?.text || 'No text available'}
                                    </p>
                                    {match.clause?.risk_level && (
                                        <span className="inline-block mt-2 text-xs px-2 py-1 bg-white rounded">
                                            Risk: {match.clause.risk_level}
                                        </span>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}

            {/* Example Queries */}
            {!results && !loading && (
                <div className="mt-6 p-4 bg-purple-50 rounded-lg">
                    <p className="text-sm font-medium text-gray-700 mb-2">
                        Try searching for:
                    </p>
                    <div className="flex flex-wrap gap-2">
                        {[
                            'payment within 30 days',
                            'termination conditions',
                            'intellectual property rights',
                            'confidentiality obligations'
                        ].map(example => (
                            <button
                                key={example}
                                onClick={() => {
                                    setSearchQuery(example);
                                    const form = new Event('submit', { cancelable: true, bubbles: true });
                                    handleSearch(form as any);
                                }}
                                className="text-xs px-3 py-1 bg-white border border-purple-300 text-purple-700 rounded-full hover:bg-purple-100 transition-colors"
                            >
                                {example}
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
