import { useState, useRef, useEffect } from 'react';
import { FaPaperPlane, FaUser, FaRobot, FaSpinner } from 'react-icons/fa';
import { sendChatMessage } from '../services/api';

function ChatInterface({ company }) {
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            content: `Hi! I've analyzed all the research data for ${company}. Ask me anything about the company!`
        }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMessage = input.trim();
        setInput('');

        // Add user message
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setLoading(true);

        try {
            const response = await sendChatMessage(company, userMessage);

            // Add assistant response
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: response.response
            }]);
        } catch (error) {
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: 'Sorry, I encountered an error processing your request. Please try again.'
            }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="glass-card p-6 max-w-4xl mx-auto">
            <div className="flex items-center gap-3 mb-6 pb-4 border-b border-white/10">
                <div className="w-10 h-10 bg-gradient-to-tr from-blue-500 to-cyan-600 rounded-lg flex items-center justify-center">
                    <FaRobot className="text-white text-xl" />
                </div>
                <div>
                    <h2 className="text-xl font-bold">AI Research Assistant</h2>
                    <p className="text-gray-400 text-sm">Chat with your {company} research data</p>
                </div>
            </div>

            {/* Messages */}
            <div className="h-[500px] overflow-y-auto custom-scrollbar mb-6 space-y-4">
                {messages.map((message, index) => (
                    <div key={index} className="flex gap-3 items-start">
                        {message.role === 'user' ? (
                            <>
                                <div className="flex-1"></div>
                                <div className="message-user">
                                    <p className="text-sm leading-relaxed">{message.content}</p>
                                </div>
                                <div className="w-8 h-8 bg-gradient-to-tr from-purple-500 to-pink-600 rounded-full flex items-center justify-center flex-shrink-0">
                                    <FaUser className="text-white text-sm" />
                                </div>
                            </>
                        ) : (
                            <>
                                <div className="w-8 h-8 bg-gradient-to-tr from-blue-500 to-cyan-600 rounded-full flex items-center justify-center flex-shrink-0">
                                    <FaRobot className="text-white text-sm" />
                                </div>
                                <div className="message-assistant">
                                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
                                </div>
                                <div className="flex-1"></div>
                            </>
                        )}
                    </div>
                ))}

                {loading && (
                    <div className="flex gap-3 items-start">
                        <div className="w-8 h-8 bg-gradient-to-tr from-blue-500 to-cyan-600 rounded-full flex items-center justify-center flex-shrink-0">
                            <FaRobot className="text-white text-sm" />
                        </div>
                        <div className="message-assistant">
                            <div className="flex items-center gap-2">
                                <FaSpinner className="animate-spin text-blue-400" />
                                <span className="text-sm text-gray-400">Thinking...</span>
                            </div>
                        </div>
                        <div className="flex-1"></div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form onSubmit={handleSubmit} className="flex gap-3">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask anything about this company..."
                    className="input-field flex-1"
                    disabled={loading}
                />
                <button
                    type="submit"
                    disabled={loading || !input.trim()}
                    className="btn-primary px-6"
                >
                    <FaPaperPlane />
                </button>
            </form>

            {/* Suggested Questions */}
            {messages.length <= 1 && (
                <div className="mt-4 flex flex-wrap gap-2">
                    <span className="text-xs text-gray-500">Try asking:</span>
                    {[
                        'What are the key products?',
                        'Recent news and updates?',
                        'Market sentiment?',
                        'What makes them unique?'
                    ].map((question, idx) => (
                        <button
                            key={idx}
                            onClick={() => setInput(question)}
                            className="text-xs bg-white/5 hover:bg-white/10 border border-white/10 rounded-full px-3 py-1 transition-colors"
                        >
                            {question}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}

export default ChatInterface;
