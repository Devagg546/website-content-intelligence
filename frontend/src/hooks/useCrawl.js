import { useState, useCallback } from 'react';
import crawlApi from '../api/crawlApi';

/**
 * Custom hook for managing crawl operations.
 * Handles starting crawls, polling status, and maintaining history.
 */
export function useCrawl() {
  const [isLoading, setIsLoading] = useState(false);
  const [crawlStatus, setCrawlStatus] = useState(null);
  const [error, setError] = useState(null);

  const startCrawl = useCallback(async (url, maxPages = 500) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await crawlApi.startCrawl(url, maxPages);
      setCrawlStatus({
        job_id: response.job_id,
        status: 'in_progress',
        pages_crawled: 0,
        pages_total: 0,
      });
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const checkStatus = useCallback(async (jobId) => {
    try {
      const status = await crawlApi.getStatus(jobId);
      setCrawlStatus(status);
      return status;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  return {
    isLoading,
    crawlStatus,
    error,
    startCrawl,
    checkStatus,
  };
}

export default useCrawl;
