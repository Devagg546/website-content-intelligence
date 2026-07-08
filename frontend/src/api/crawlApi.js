/**
 * Crawl API — Start and monitor website crawl jobs.
 */
import apiClient from './client';

export const crawlApi = {
  /** Start a new crawl job */
  startCrawl: (url, maxPages = 500) =>
    apiClient.post('/crawl', { url, max_pages: maxPages }),

  /** Get crawl job status */
  getStatus: (jobId) =>
    apiClient.get(`/crawl/status/${jobId}`),

  /** Get crawl history */
  getHistory: () =>
    apiClient.get('/crawl/history'),
};

export default crawlApi;
