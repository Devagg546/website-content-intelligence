/**
 * Stats grid — displays key metrics in a responsive grid.
 */
function StatsGrid({ stats = [] }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat, idx) => (
        <div
          key={idx}
          className="glass-card p-5 animate-slide-up"
          style={{ animationDelay: `${idx * 50}ms` }}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-surface-400">{stat.label}</p>
              <p className="text-2xl font-bold text-surface-100 mt-1">
                {stat.value}
              </p>
            </div>
            {stat.icon && (
              <div className="w-10 h-10 rounded-lg bg-brand-500/10 flex items-center justify-center">
                <span className="text-xl">{stat.icon}</span>
              </div>
            )}
          </div>
          {stat.change && (
            <p className={`text-xs mt-2 ${stat.change > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
              {stat.change > 0 ? '↑' : '↓'} {Math.abs(stat.change)}%
            </p>
          )}
        </div>
      ))}
    </div>
  );
}

export default StatsGrid;
