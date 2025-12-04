import { useState } from 'react';
import { FaSearch, FaBrain, FaChartLine } from 'react-icons/fa';
import ResearchForm from './components/ResearchForm';
import ChatInterface from './components/ChatInterface';
import Visualization from './components/Visualization';

function App() {
    const [step, setStep] = useState('research'); // research | chat
    const [currentCompany, setCurrentCompany] = useState('');
    const [vizData, setVizData] = useState(null);

    const handleResearchComplete = (company, data) => {
        setCurrentCompany(company);
        setVizData(data);
        setStep('chat');
    };

    const handleStartNew = () => {
        setStep('research');
        setCurrentCompany('');
        setVizData(null);
    };

    return (
        <div className="min-h-screen pb-10">
            {/* Header */}
            <header className="pt-8 pb-6 px-4">
                <div className="max-w-7xl mx-auto">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <div className="w-12 h-12 bg-gradient-to-tr from-purple-500 to-pink-600 rounded-xl flex items-center justify-center shadow-lg shadow-purple-500/30">
                                <FaBrain className="text-2xl text-white" />
                            </div>
                            <div>
                                <h1 className="text-3xl font-bold gradient-text">InsightFlow</h1>
                                <p className="text-gray-400 text-sm">AI-Powered Company Research</p>
                            </div>
                        </div>

                        {currentCompany && (
                            <button
                                onClick={handleStartNew}
                                className="btn-secondary text-sm"
                            >
                                New Research
                            </button>
                        )}
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4">
                {step === 'research' ? (
                    <div className="space-y-8">
                        <div className="text-center max-w-2xl mx-auto mb-12">
                            <div className="inline-flex items-center gap-2 bg-purple-500/20 border border-purple-500/30 rounded-full px-4 py-2 mb-4">
                                <FaChartLine className="text-purple-400" />
                                <span className="text-sm text-purple-300">Autonomous AI Research Engine</span>
                            </div>
                            <h2 className="text-4xl md:text-5xl font-bold mb-4">
                                Discover Real-Time{' '}
                                <span className="gradient-text">Company Insights</span>
                            </h2>
                            <p className="text-gray-300 text-lg">
                                Enter a company name and let our AI agents gather and analyze comprehensive data from multiple sources.
                            </p>
                        </div>

                        <ResearchForm onResearchComplete={handleResearchComplete} />

                        {/* Features Grid */}
                        <div className="grid md:grid-cols-3 gap-6 mt-16">
                            <div className="glass-card p-6 transform hover:scale-105 transition-transform duration-200">
                                <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center mb-4">
                                    <FaSearch className="text-2xl text-purple-400" />
                                </div>
                                <h3 className="text-xl font-semibold mb-2">Multi-Source Collection</h3>
                                <p className="text-gray-400">
                                    Aggregates data from news, Reddit, GitHub, and web sources automatically.
                                </p>
                            </div>

                            <div className="glass-card p-6 transform hover:scale-105 transition-transform duration-200">
                                <div className="w-12 h-12 bg-pink-500/20 rounded-lg flex items-center justify-center mb-4">
                                    <FaBrain className="text-2xl text-pink-400" />
                                </div>
                                <h3 className="text-xl font-semibold mb-2">AI Analysis</h3>
                                <p className="text-gray-400">
                                    Advanced AI processes and summarizes information into actionable insights.
                                </p>
                            </div>

                            <div className="glass-card p-6 transform hover:scale-105 transition-transform duration-200">
                                <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-4">
                                    <FaChartLine className="text-2xl text-blue-400" />
                                </div>
                                <h3 className="text-xl font-semibold mb-2">Interactive Chat</h3>
                                <p className="text-gray-400">
                                    Chat with your research data using natural language queries.
                                </p>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="space-y-6">
                        {vizData && <Visualization data={vizData} company={currentCompany} />}
                        <ChatInterface company={currentCompany} />
                    </div>
                )}
            </main>

            {/* Footer */}
            <footer className="mt-20 text-center text-gray-500 text-sm">
                <p>© 2024 InsightFlow. Powered by AI Innovation.</p>
            </footer>
        </div>
    );
}

export default App;
