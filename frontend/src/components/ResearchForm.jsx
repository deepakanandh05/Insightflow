import { useState } from 'react';
import { FaRocket, FaSpinner } from 'react-icons/fa';
import { researchCompany } from '../services/api';

function ResearchForm({ onResearchComplete }) {
    const [companyName, setCompanyName] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [progress, setProgress] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!companyName.trim()) return;

        setLoading(true);
        setError('');
        setProgress('Initializing AI agents...');

        try {
            const simulateProgress = [
                'Searching for company data...',
                'Planning data collection strategy...',
                'Fetching from multiple sources...',
                'Cleaning and processing data...',
                'Storing in vector database...',
                'Generating insights and summary...'
            ];

            let currentStep = 0;
            const progressInterval = setInterval(() => {
                if (currentStep < simulateProgress.length) {
                    setProgress(simulateProgress[currentStep]);
                    currentStep++;
                }
            }, 3000);

            const response = await researchCompany(companyName);

            clearInterval(progressInterval);
            setProgress('Research complete!');

            setTimeout(() => {
                onResearchComplete(companyName, response.viz_data);
            }, 500);

        } catch (err) {
            setError(err.response?.data?.error || 'Failed to research company. Please try again.');
            setProgress('');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto">
            <form onSubmit={handleSubmit} className="glass-card p-8">
                <div className="space-y-6">
                    <div>
                        <label htmlFor="company" className="block text-sm font-medium mb-2 text-gray-300">
                            Company Name
                        </label>
                        <input
                            id="company"
                            type="text"
                            value={companyName}
                            onChange={(e) => setCompanyName(e.target.value)}
                            placeholder="e.g., OpenAI, Tesla, Microsoft..."
                            className="input-field"
                            disabled={loading}
                            required
                        />
                    </div>

                    {error && (
                        <div className="bg-red-500/20 border border-red-500/30 rounded-xl p-4 text-red-300 text-sm">
                            {error}
                        </div>
                    )}

                    {loading && progress && (
                        <div className="bg-purple-500/20 border border-purple-500/30 rounded-xl p-4">
                            <div className="flex items-center gap-3 mb-2">
                                <FaSpinner className="text-purple-400 animate-spin" />
                                <span className="text-purple-300 font-medium">{progress}</span>
                            </div>
                            <div className="w-full bg-white/10 rounded-full h-2 mt-3">
                                <div className="bg-gradient-to-r from-purple-500 to-pink-600 h-2 rounded-full shimmer"></div>
                            </div>
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={loading || !companyName.trim()}
                        className="btn-primary w-full flex items-center justify-center gap-2"
                    >
                        {loading ? (
                            <>
                                <FaSpinner className="animate-spin" />
                                <span>Researching...</span>
                            </>
                        ) : (
                            <>
                                <FaRocket />
                                <span>Start Research</span>
                            </>
                        )}
                    </button>
                </div>
            </form>

            {!loading && (
                <div className="mt-6 text-center text-gray-400 text-sm">
                    <p>💡 Try: "Google", "Apple", "SpaceX", or any company name</p>
                </div>
            )}
        </div>
    );
}

export default ResearchForm;
