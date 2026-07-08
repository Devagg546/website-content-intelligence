import { useState, useEffect } from 'react';
import Spinner from '../components/common/Spinner';
import GapSummary from '../components/gaps/GapSummary';
import GapTable from '../components/gaps/GapTable';
import gapsApi from '../api/gapsApi';

/**
 * Gaps Page — /gaps
 * Content gap detection and SEO issue reporting.
 */
function GapsPage() {
  const [gaps, setGaps] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

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

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <GapSummary gaps={gaps || {}} />

      {/* Detailed Issue Lists */}
      <GapTable items={gaps?.missing_title || []} title="Missing Page Titles" />
      <GapTable items={gaps?.missing_meta_description || []} title="Missing Meta Descriptions" />
      <GapTable items={gaps?.missing_h1 || []} title="Missing H1 Tags" />
      <GapTable items={gaps?.thin_content || []} title="Thin Content" />
      <GapTable items={gaps?.orphan_pages || []} title="Orphan Pages" />

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
