import { useState, useEffect } from 'react';
import Card from '../components/common/Card';
import Spinner from '../components/common/Spinner';
import StatsGrid from '../components/dashboard/StatsGrid';
import ContentTable from '../components/dashboard/ContentTable';
import inventoryApi from '../api/inventoryApi';

/**
 * Dashboard Page — /dashboard
 * Content inventory with statistics, tables, and charts.
 */
function DashboardPage() {
  const [inventory, setInventory] = useState(null);
  const [pages, setPages] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setIsLoading(true);
    try {
      const [inventoryData, pagesData] = await Promise.all([
        inventoryApi.getInventory(),
        inventoryApi.getPages(1, 20),
      ]);
      setInventory(inventoryData);
      setPages(pagesData.pages || []);
    } catch (error) {
      console.error('Failed to load dashboard:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Spinner size="lg" label="Loading dashboard..." className="py-20" />;
  }

  const stats = [
    { label: 'Total Pages', value: inventory?.total_pages || 0, icon: '📄' },
    { label: 'Total Words', value: (inventory?.total_words || 0).toLocaleString(), icon: '📝' },
    { label: 'Avg. Words/Page', value: Math.round(inventory?.avg_content_length || 0), icon: '📊' },
    { label: 'Top Keywords', value: inventory?.top_keywords?.length || 0, icon: '🔑' },
  ];

  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <StatsGrid stats={stats} />

      {/* Top Keywords */}
      {inventory?.top_keywords?.length > 0 && (
        <Card>
          <Card.Header title="Top Keywords" subtitle="Most frequently used terms" />
          <div className="flex flex-wrap gap-2">
            {inventory.top_keywords.slice(0, 20).map((kw, idx) => (
              <span
                key={idx}
                className="px-3 py-1 rounded-full bg-surface-800 text-surface-300 text-sm border border-surface-700"
              >
                {kw.keyword} ({kw.count})
              </span>
            ))}
          </div>
        </Card>
      )}

      {/* Pages Table */}
      <Card>
        <Card.Header
          title="Crawled Pages"
          subtitle={`${pages.length} pages loaded`}
        />
        <ContentTable pages={pages} />
      </Card>
    </div>
  );
}

export default DashboardPage;
