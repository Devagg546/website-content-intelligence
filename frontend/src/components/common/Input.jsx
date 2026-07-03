/**
 * Reusable Input component with label and error state.
 */
function Input({
  label,
  error,
  id,
  className = '',
  ...props
}) {
  return (
    <div className={className}>
      {label && (
        <label htmlFor={id} className="block text-sm font-medium text-surface-300 mb-1.5">
          {label}
        </label>
      )}
      <input
        id={id}
        className={`input-field ${error ? 'border-red-500 focus:ring-red-500/40' : ''}`}
        {...props}
      />
      {error && (
        <p className="mt-1 text-xs text-red-400">{error}</p>
      )}
    </div>
  );
}

export default Input;
