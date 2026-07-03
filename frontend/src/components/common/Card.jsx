/**
 * Card container with optional glassmorphism effect.
 */
function Card({ children, className = '', hoverable = false, ...props }) {
  const hoverClass = hoverable ? 'glass-card-hover' : 'glass-card';

  return (
    <div className={`${hoverClass} p-6 ${className}`} {...props}>
      {children}
    </div>
  );
}

/**
 * Card header with title and optional action.
 */
function CardHeader({ title, subtitle, action, className = '' }) {
  return (
    <div className={`flex items-start justify-between mb-4 ${className}`}>
      <div>
        <h3 className="text-lg font-semibold text-surface-100">{title}</h3>
        {subtitle && (
          <p className="text-sm text-surface-400 mt-0.5">{subtitle}</p>
        )}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}

Card.Header = CardHeader;

export default Card;
