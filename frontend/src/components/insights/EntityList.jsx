/**
 * Entity list — displays frequently mentioned entities grouped by type.
 */
function EntityList({ entities = {} }) {
  const entityTypes = [
    { key: 'brands', label: 'Brands', icon: '🏢' },
    { key: 'locations', label: 'Locations', icon: '📍' },
    { key: 'services', label: 'Services', icon: '🛎️' },
    { key: 'products', label: 'Products', icon: '📦' },
  ];

  const hasEntities = entityTypes.some(
    ({ key }) => entities[key] && entities[key].length > 0
  );

  if (!hasEntities) {
    return (
      <p className="text-sm text-surface-500 text-center py-8">
        No entities extracted yet.
      </p>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {entityTypes.map(({ key, label, icon }) => {
        const items = entities[key] || [];
        if (items.length === 0) return null;

        return (
          <div key={key} className="glass-card p-4">
            <h4 className="text-sm font-medium text-surface-200 mb-3">
              {icon} {label}
            </h4>
            <div className="space-y-2">
              {items.slice(0, 10).map((entity, idx) => (
                <div
                  key={idx}
                  className="flex items-center justify-between text-sm"
                >
                  <span className="text-surface-300">{entity.name}</span>
                  <span className="text-surface-500">{entity.count} mentions</span>
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default EntityList;
