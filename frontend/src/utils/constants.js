/**
 * Application constants.
 */

/** API base URL (from environment or default) */
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

/** Maximum number of pages to crawl */
export const MAX_CRAWL_PAGES = 500;

/** Polling interval for crawl status (ms) */
export const CRAWL_POLL_INTERVAL = 2000;

/** Search result limit */
export const DEFAULT_SEARCH_LIMIT = 20;

/** Crawl status values */
export const CRAWL_STATUS = {
  QUEUED: 'queued',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  FAILED: 'failed',
};

/** Search types */
export const SEARCH_TYPES = {
  KEYWORD: 'keyword',
  SEMANTIC: 'semantic',
  HYBRID: 'hybrid',
};

/** Gap severity levels */
export const SEVERITY = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  CRITICAL: 'critical',
};
