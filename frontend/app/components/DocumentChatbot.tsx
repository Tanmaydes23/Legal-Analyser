import React from 'react';

interface DocumentChatbotProps {
    documentId: string;
    documentText: string;
    analysis: any;
}

interface Message {
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
}

export default function DocumentChatbot({ documentId, documentText, analysis }: DocumentChatbotProps) {
    const [messages, setMessages] = React.useState<Message[]>([
        {
            role: 'assistant',
            content: 'Hi! I\'m your AI legal assistant. Ask me anything about this document, its clauses, risks, or compliance requirements.',
            timestamp: new Date()
        }
    ]);
    const [input, setInput] = React.useState('');
    const [loading, setLoading] = React.useState(false);
    const messagesEndRef = React.useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    React.useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || loading) return;

        const userMessage: Message = {
            role: 'user',
            content: input,
            timestamp: new Date()
        };

        setMessages([...messages, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const response = await fetch('http://localhost:8000/api/chat/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    document_id: documentId,
                    question: input,
                    document_text: documentText.substring(0, 3000), // First 3000 chars
                    analysis_summary: analysis?.ai_summary?.summary || ''
                })
            });

            const data = await response.json();

            const assistantMessage: Message = {
                role: 'assistant',
                content: data.answer || 'Sorry, I couldn\'t process that question.',
                timestamp: new Date()
            };

            setMessages(prev => [...prev, assistantMessage]);
        } catch (error) {
            console.error('Chat error:', error);
            const errorMessage: Message = {
                role: 'assistant',
                content: 'Sorry, there was an error processing your question. Please try again.',
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const suggestedQuestions = [
        'What are the main risks in this document?',
        'Are there any missing clauses?',
        'What Indian laws apply to this contract?',
        'Summarize the payment terms',
        'What is the termination clause?'
    ];

    return (
        <div className="bg-white rounded-lg shadow-md overflow-hidden mb-6">
            {/* Header */}
            <div className="bg-gradient-to-r from-purple-600 to-blue-600 p-4">
                <h3 className="text-xl font-bold text-white flex items-center gap-2">
                    💬 AI Legal Assistant
                    <span className="text-xs font-normal bg-white/20 px-2 py-1 rounded">
                        Powered by Groq LLM
                    </span>
                </h3>
                <p className="text-sm text-white/80 mt-1">
                    Ask questions about your document
                </p>
            </div>

            {/* Messages */}
            <div className="h-96 overflow-y-auto p-4 bg-gray-50">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`mb-4 flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div
                            className={`max-w-[80%] rounded-lg p-3 ${msg.role === 'user'
                                    ? 'bg-purple-600 text-white'
                                    : 'bg-white border border-gray-200 text-gray-800'
                                }`}
                        >
                            <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                            <p className={`text-xs mt-1 ${msg.role === 'user' ? 'text-purple-200' : 'text-gray-400'}`}>
                                {msg.timestamp.toLocaleTimeString()}
                            </p>
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex justify-start mb-4">
                        <div className="bg-white border border-gray-200 rounded-lg p-3">
                            <div className="flex gap-1">
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                            </div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Suggested Questions */}
            {messages.length === 1 && (
                <div className="p-4 border-t border-gray-200 bg-purple-50">
                    <p className="text-sm font-medium text-gray-700 mb-2">💡 Try asking:</p>
                    <div className="flex flex-wrap gap-2">
                        {suggestedQuestions.map((q, idx) => (
                            <button
                                key={idx}
                                onClick={() => setInput(q)}
                                className="text-xs px-3 py-1 bg-white border border-purple-300 text-purple-700 rounded-full hover:bg-purple-100 transition-colors"
                            >
                                {q}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Input */}
            <div className="p-4 border-t border-gray-200 bg-white">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Ask a question about this document..."
                        disabled={loading}
                        className="flex-1 px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-purple-500 focus:outline-none disabled:opacity-50"
                    />
                    <button
                        onClick={handleSend}
                        disabled={loading || !input.trim()}
                        className="px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-lg hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                    >
                        {loading ? 'Sending...' : 'Send'}
                    </button>
                </div>
            </div>
        </div>
    );
}
