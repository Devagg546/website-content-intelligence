/**
 * Citation card — displays a source reference for AI answers.
 * Shows page title, URL, and a relevant text snippet.
 */
function CitationCard({ citation }) {
  const { page_title, url, snippet, relevance_score } = citation;

  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className="block p-2.5 rounded-lg bg-surface-700/50 border border-surface-600/50 hover:border-brand-500/30 transition-colors group"
    >
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0 flex-1">
          <p className="text-xs font-medium text-brand-400 group-hover:text-brand-300 truncate">
            {page_title || 'Untitled Page'}
          </p>
          <p className="text-xs text-surface-500 truncate mt-0.5">{url}</p>
        </div>
        {relevance_score > 0 && (
          <span className="text-xs text-surface-500 flex-shrink-0">
            {Math.round(relevance_score * 100)}%
          </span>
        )}
      </div>
      {snippet && (
        <p className="text-xs text-surface-400 mt-1.5 line-clamp-2">{snippet}</p>
      )}
    </a>
  );
}

export default CitationCard;
