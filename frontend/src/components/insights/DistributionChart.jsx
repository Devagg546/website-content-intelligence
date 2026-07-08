/**
 * Content distribution chart — horizontal bar chart for topic percentages.
 * Uses a simple CSS-based chart (no chart library dependency for this component).
 */
function DistributionChart({ data = [] }) {
  if (data.length === 0) {
    return (
      <p className="text-sm text-surface-500 text-center py-8">
        No distribution data available.
      </p>
    );
  }

  const colors = [
    'bg-brand-500', 'bg-emerald-500', 'bg-amber-500', 'bg-purple-500',
    'bg-rose-500', 'bg-cyan-500', 'bg-orange-500', 'bg-indigo-500',
  ];

  return (
    <div className="space-y-3">
      {data.map((item, idx) => (
        <div key={idx} className="flex items-center gap-3">
          <span className="text-sm text-surface-300 w-32 truncate">{item.topic}</span>
          <div className="flex-1 h-6 bg-surface-800 rounded-full overflow-hidden">
            <div
              className={`h-full ${colors[idx % colors.length]} rounded-full transition-all duration-700 ease-out`}
              style={{ width: `${item.percentage}%` }}
            />
          </div>
          <span className="text-sm text-surface-400 w-12 text-right">
            {item.percentage.toFixed(1)}%
          </span>
        </div>
      ))}
    </div>
  );
}

export default DistributionChart;
