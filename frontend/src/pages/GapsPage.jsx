import { useState, useEffect } from 'react';
import Spinner from '../components/common/Spinner';
import GapSummary from '../components/gaps/GapSummary';
import GapTable from '../components/gaps/GapTable';
import gapsApi from '../api/gapsApi';

const LABELS = {
  missing_title: 'Missing Page Titles',
  missing_meta_description: 'Missing Meta Descriptions',
  missing_h1: 'Missing H1 Tags',
  thin_content: 'Thin Content',
  duplicate_content: 'Duplicate Content',
  orphan_pages: 'Orphan Pages',
};

function GapsPage() {
  const [gaps, setGaps] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedKey, setSelectedKey] = useState('missing_title');

  useEffect(() => {
    loadGaps();
  }, []);

  const loadGaps = async () => {
    setIsLoading(true);
    try {
      const data = await gapsApi.getGaps();
      setGaps(data);
    } catch (error) {
      console.error('Failed to load gaps:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Spinner size="lg" label="Analyzing content gaps..." className="py-20" />;
  }

  const selectedItems = gaps?.[selectedKey] || [];
  const isDuplicates = selectedKey === 'duplicate_content';

  return (
    <div className="space-y-6">
      {/* Summary Cards — clickable */}
      <GapSummary gaps={gaps || {}} selectedKey={selectedKey} onSelect={setSelectedKey} />

      {/* Selected category's details only */}
      {isDuplicates ? (
        selectedItems.length > 0 ? (
          <div className="glass-card p-6 space-y-3">
            <h3 className="text-lg font-semibold text-surface-100">
              {LABELS[selectedKey]} ({selectedItems.length})
            </h3>
            <div className="space-y-2">
              {selectedItems.map((pair, idx) => (
                <div
                  key={idx}
                  className="p-4 rounded-lg bg-surface-800/40 border border-surface-700/30"
                >
                  <div className="flex items-center justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-surface-300 truncate">{pair.url_a}</p>
                      <p className="text-xs text-surface-500 mt-1">vs</p>
                      <p className="text-sm text-surface-300 truncate">{pair.url_b}</p>
                    </div>
                    <span className="px-2 py-1 rounded-full bg-amber-500/10 text-amber-400 text-xs font-medium whitespace-nowrap">
                      {Math.round(pair.similarity_score * 100)}% similar
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="glass-card p-8 text-center text-sm text-surface-500">
            No duplicate content detected. ✅
          </div>
        )
      ) : (
        <GapTable items={selectedItems} title={LABELS[selectedKey]} />
      )}

      {/* Total Issues */}
      {gaps && (
        <div className="text-center py-4">
          <p className="text-sm text-surface-400">
            Total issues detected: <span className="text-surface-200 font-semibold">{gaps.total_issues}</span>
          </p>
        </div>
      )}
    </div>
  );
}

export default GapsPage;