/**
 * Empty state placeholder for sections with no data.
 */
function EmptyState({
  icon,
  title = 'No data available',
  description = 'Get started by crawling a website.',
  action,
  className = '',
}) {
  return (
    <div className={`flex flex-col items-center justify-center py-16 ${className}`}>
      {icon && (
        <div className="w-16 h-16 rounded-2xl bg-surface-800 flex items-center justify-center mb-4">
          <span className="text-3xl text-surface-500">{icon}</span>
        </div>
      )}
      <h3 className="text-lg font-medium text-surface-300 mb-1">{title}</h3>
      <p className="text-sm text-surface-500 text-center max-w-sm mb-6">
        {description}
      </p>
      {action && <div>{action}</div>}
    </div>
  );
}

export default EmptyState;
