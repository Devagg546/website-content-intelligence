import EmptyState from '../common/EmptyState';

/**
 * Search results list with highlighted snippets.
 */
function SearchResults({ results = [], query = '' }) {
  if (results.length === 0) {
    return (
      <EmptyState
        icon="🔍"
        title="No results found"
        description={query ? `No content matching "${query}"` : 'Enter a search query above.'}
      />
    );
  }

  return (
    <div className="space-y-3">
      <p className="text-sm text-surface-400">{results.length} results found</p>

      {results.map((result, idx) => (
        <a
          key={idx}
          href={result.url}
          target="_blank"
          rel="noopener noreferrer"
          className="block p-4 rounded-lg bg-surface-800/40 border border-surface-700/30 hover:border-brand-500/30 transition-colors group"
        >
          <h4 className="text-sm font-medium text-brand-400 group-hover:text-brand-300">
            {result.page_title || 'Untitled'}
          </h4>
          <p className="text-xs text-surface-500 mt-0.5 truncate">{result.url}</p>
          <p className="text-sm text-surface-300 mt-2 line-clamp-3">{result.snippet}</p>
          {result.score > 0 && (
            <p className="text-xs text-surface-500 mt-2">
              Relevance: {Math.round(result.score * 100)}%
            </p>
          )}
        </a>
      ))}
    </div>
  );
}

export default SearchResults;
