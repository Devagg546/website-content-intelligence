import { useState } from 'react';
import Card from '../components/common/Card';
import CrawlForm from '../components/crawl/CrawlForm';
import CrawlProgress from '../components/crawl/CrawlProgress';
import CrawlHistory from '../components/crawl/CrawlHistory';
import crawlApi from '../api/crawlApi';

/**
 * Crawl Page — /crawl
 * URL input, crawl progress tracking, and crawl history.
 */
function CrawlPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [crawlStatus, setCrawlStatus] = useState(null);
  const [crawlHistory, setCrawlHistory] = useState([]);

  const handleStartCrawl = async ({ url, maxPages }) => {
    setIsLoading(true);
    try {
      const response = await crawlApi.startCrawl(url, maxPages);
      setCrawlStatus({
        job_id: response.job_id,
        status: 'in_progress',
        pages_crawled: 0,
        pages_total: 0,
      });
      // TODO: Start polling for status updates
    } catch (error) {
      console.error('Failed to start crawl:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Crawl Form */}
        <Card>
          <Card.Header
            title="Start New Crawl"
            subtitle="Enter a website URL to begin crawling and indexing"
          />
          <CrawlForm onSubmit={handleStartCrawl} isLoading={isLoading} />
        </Card>

        {/* Crawl Progress */}
        <Card>
          <Card.Header
            title="Crawl Progress"
            subtitle="Real-time crawling status"
          />
          {crawlStatus ? (
            <CrawlProgress status={crawlStatus} />
          ) : (
            <p className="text-sm text-surface-500 text-center py-8">
              No active crawl. Start one to see progress here.
            </p>
          )}
        </Card>
      </div>

      {/* Crawl History */}
      <Card>
        <Card.Header
          title="Crawl History"
          subtitle="Previous crawl jobs and their results"
        />
        <CrawlHistory jobs={crawlHistory} />
      </Card>
    </div>
  );
}

export default CrawlPage;
