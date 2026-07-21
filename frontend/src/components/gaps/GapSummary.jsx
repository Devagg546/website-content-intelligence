import Badge from '../common/Badge';

/**
 * Gap summary — overview cards showing issue counts by category.
 * Clicking a card selects that category to view details below.
 */
function GapSummary({ gaps = {}, selectedKey, onSelect }) {
  const categories = [
    { key: 'missing_title', label: 'Missing Title', icon: '📄', severity: 'error' },
    { key: 'missing_meta_description', label: 'Missing Meta Description', icon: '📝', severity: 'warning' },
    { key: 'missing_h1', label: 'Missing H1', icon: '🏷️', severity: 'warning' },
    { key: 'thin_content', label: 'Thin Content', icon: '📉', severity: 'warning' },
    { key: 'duplicate_content', label: 'Duplicate Content', icon: '📋', severity: 'error' },
    { key: 'orphan_pages', label: 'Orphan Pages', icon: '🔗', severity: 'info' },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {categories.map(({ key, label, icon, severity }) => {
        const items = gaps[key] || [];
        const count = items.length;
        const isSelected = selectedKey === key;

        return (
          <button
            key={key}
            onClick={() => onSelect(key)}
            className={`glass-card p-4 text-left transition-all ${
              isSelected
                ? 'ring-2 ring-brand-500 border-brand-500/50'
                : 'hover:border-surface-600'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-lg">{icon}</span>
              <Badge variant={count > 0 ? severity : 'success'}>
                {count > 0 ? `${count} issues` : 'Clean'}
              </Badge>
            </div>
            <p className="text-sm font-medium text-surface-200">{label}</p>
            <p className="text-xs text-surface-500 mt-0.5">
              {count > 0 ? `${count} pages affected` : 'No issues detected'}
            </p>
          </button>
        );
      })}
    </div>
  );
}

export default GapSummary;