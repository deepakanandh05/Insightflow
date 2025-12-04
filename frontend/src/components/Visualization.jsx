import { FaChartPie, FaDatabase, FaLightbulb } from 'react-icons/fa';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

function Visualization({ data, company }) {
    if (!data) return null;

    const { summary, sources_breakdown, total_sources } = data;

    // Prepare data for pie chart
    const chartData = Object.entries(sources_breakdown || {}).map(([name, value]) => ({
        name: name.charAt(0).toUpperCase() + name.slice(1),
        value: value
    }));

    const COLORS = ['#a855f7', '#ec4899', '#f97316', '#3b82f6', '#10b981', '#f59e0b'];

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            return (
                <div className="glass-card p-3">
                    <p className="text-sm font-semibold">{payload[0].name}</p>
                    <p className="text-xs text-gray-400">{payload[0].value} sources</p>
                </div>
            );
        }
        return null;
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="glass-card p-6">
                <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 bg-gradient-to-tr from-green-500 to-emerald-600 rounded-lg flex items-center justify-center">
                        <FaLightbulb className="text-white text-xl" />
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold">{company}</h2>
                        <p className="text-gray-400 text-sm">Research Summary</p>
                    </div>
                </div>

                {/* Summary */}
                <div className="bg-white/5 rounded-xl p-6 mt-4 border border-white/10">
                    <p className="text-gray-200 leading-relaxed whitespace-pre-wrap">{summary}</p>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid md:grid-cols-2 gap-6">
                {/* Data Sources Chart */}
                <div className="glass-card p-6">
                    <div className="flex items-center gap-2 mb-4">
                        <FaChartPie className="text-purple-400" />
                        <h3 className="text-lg font-semibold">Data Sources</h3>
                    </div>

                    <ResponsiveContainer width="100%" height={250}>
                        <PieChart>
                            <Pie
                                data={chartData}
                                cx="50%"
                                cy="50%"
                                labelLine={false}
                                label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                                outerRadius={80}
                                fill="#8884d8"
                                dataKey="value"
                            >
                                {chartData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Pie>
                            <Tooltip content={<CustomTooltip />} />
                        </PieChart>
                    </ResponsiveContainer>
                </div>

                {/* Stats Card */}
                <div className="glass-card p-6">
                    <div className="flex items-center gap-2 mb-4">
                        <FaDatabase className="text-pink-400" />
                        <h3 className="text-lg font-semibold">Collection Stats</h3>
                    </div>

                    <div className="space-y-4 mt-6">
                        <div className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 border border-purple-500/30 rounded-xl p-4">
                            <div className="text-3xl font-bold gradient-text">{total_sources}</div>
                            <div className="text-sm text-gray-400 mt-1">Total Data Points</div>
                        </div>

                        <div className="space-y-2">
                            {Object.entries(sources_breakdown || {}).map(([source, count]) => (
                                <div key={source} className="flex justify-between items-center bg-white/5 rounded-lg px-4 py-3">
                                    <span className="text-sm capitalize text-gray-300">{source}</span>
                                    <span className="font-semibold text-purple-400">{count}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Visualization;
