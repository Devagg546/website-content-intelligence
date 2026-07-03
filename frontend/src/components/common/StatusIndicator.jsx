/**
 * Live status indicator dot with label.
 */
function StatusIndicator({ status = 'offline', label, className = '' }) {
  const statusColors = {
    online: 'bg-emerald-400',
    offline: 'bg-surface-500',
    processing: 'bg-amber-400 animate-pulse',
    error: 'bg-red-400',
  };

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <div className={`w-2 h-2 rounded-full ${statusColors[status]}`} />
      {label && <span className="text-xs text-surface-400">{label}</span>}
    </div>
  );
}

export default StatusIndicator;
