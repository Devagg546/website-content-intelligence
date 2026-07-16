import { useState } from 'react';
import Card from '../components/common/Card';
import CrawlForm from '../components/crawl/CrawlForm';
import CrawlProgress from '../components/crawl/CrawlProgress';
import CrawlHistory from '../components/crawl/CrawlHistory';
import crawlApi from '../api/crawlApi';
import { useAppContext } from '../context/AppContext';

function CrawlPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [crawlHistory, setCrawlHistory] = useState([]);
  
  // Use global context so state persists when switching pages
  const { activeCrawlJobId, setActiveCrawlJobId, crawlStatus, setCrawlStatus } = useAppContext();

  const handleStartCrawl = async ({ url, maxPages }) => {
    setIsLoading(true);
    try {
      const response = await crawlApi.startCrawl(url, maxPages);
      const jobId = response.job_id;

      setActiveCrawlJobId(jobId);
      setCrawlStatus({
        job_id: jobId,
        status: 'in_progress',
        pages_crawled: 0,
        pages_total: maxPages,
      });

      const interval = setInterval(async () => {
        try {
          const statusResponse = await crawlApi.getStatus(jobId);
          setCrawlStatus(statusResponse);
          if (statusResponse.status === 'completed' || statusResponse.status === 'failed') {
            clearInterval(interval);
            setIsLoading(false);
          }
        } catch (err) {
          clearInterval(interval);
          setIsLoading(false);
        }
      }, 3000);

    } catch (error) {
      console.error('Failed to start crawl:', error);
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <Card.Header
            title="Start New Crawl"
            subtitle="Enter a website URL to begin crawling and indexing"
          />
          <CrawlForm onSubmit={handleStartCrawl} isLoading={isLoading} />
        </Card>

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