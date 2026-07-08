/**
 * Content table — sortable page listing.
 */
function ContentTable({ pages = [], onPageClick }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-surface-700">
            <th className="text-left py-3 px-4 text-xs font-medium text-surface-400 uppercase tracking-wider">
              Page
            </th>
            <th className="text-left py-3 px-4 text-xs font-medium text-surface-400 uppercase tracking-wider">
              Title
            </th>
            <th className="text-right py-3 px-4 text-xs font-medium text-surface-400 uppercase tracking-wider">
              Words
            </th>
            <th className="text-right py-3 px-4 text-xs font-medium text-surface-400 uppercase tracking-wider">
              Status
            </th>
          </tr>
        </thead>
        <tbody>
          {pages.map((page, idx) => (
            <tr
              key={idx}
              onClick={() => onPageClick?.(page)}
              className="border-b border-surface-800/50 hover:bg-surface-800/30 transition-colors cursor-pointer"
            >
              <td className="py-3 px-4">
                <p className="text-surface-300 truncate max-w-xs">{page.url}</p>
              </td>
              <td className="py-3 px-4">
                <p className="text-surface-200 truncate max-w-xs">{page.title || '—'}</p>
              </td>
              <td className="py-3 px-4 text-right text-surface-400">
                {page.word_count?.toLocaleString() || 0}
              </td>
              <td className="py-3 px-4 text-right">
                <span className={`text-xs ${page.title && page.meta_description ? 'text-emerald-400' : 'text-amber-400'}`}>
                  {page.title && page.meta_description ? '✓ Complete' : '⚠ Incomplete'}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {pages.length === 0 && (
        <p className="text-center text-surface-500 py-8 text-sm">
          No pages crawled yet.
        </p>
      )}
    </div>
  );
}

export default ContentTable;
