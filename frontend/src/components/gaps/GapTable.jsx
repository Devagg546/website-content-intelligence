import Badge from '../common/Badge';

/**
 * Detailed gap listing table — shows individual issues with severity.
 */
function GapTable({ items = [], title = 'Issues' }) {
  if (items.length === 0) {
    return null;
  }

  return (
    <div className="glass-card p-4">
      <h4 className="text-sm font-medium text-surface-200 mb-3">{title} ({items.length})</h4>
      <div className="space-y-2">
        {items.map((item, idx) => (
          <div
            key={idx}
            className="flex items-center justify-between p-2.5 rounded-lg bg-surface-800/30 border border-surface-700/20"
          >
            <div className="min-w-0 flex-1">
              <p className="text-sm text-surface-300 truncate">{item.url}</p>
              {item.title && (
                <p className="text-xs text-surface-500 truncate">{item.title}</p>
              )}
            </div>
            <Badge variant={item.severity === 'high' || item.severity === 'critical' ? 'error' : 'warning'}>
              {item.severity || 'medium'}
            </Badge>
          </div>
        ))}
      </div>
    </div>
  );
}

export default GapTable;
