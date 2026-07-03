import Badge from '../common/Badge';
import { formatDate } from '../../utils/formatters';

/**
 * List of past crawl jobs with status and summary.
 */
function CrawlHistory({ jobs = [] }) {
  if (jobs.length === 0) {
    return (
      <p className="text-sm text-surface-500 text-center py-8">
        No crawl history yet. Start your first crawl above.
      </p>
    );
  }

  return (
    <div className="space-y-3">
      {jobs.map((job) => (
        <div
          key={job.job_id}
          className="flex items-center justify-between p-3 rounded-lg bg-surface-800/40 border border-surface-700/30"
        >
          <div className="min-w-0 flex-1">
            <p className="text-sm font-medium text-surface-200 truncate">
              {job.url || job.root_url}
            </p>
            <p className="text-xs text-surface-500">
              {job.pages_crawled} pages • {formatDate(job.started_at)}
            </p>
          </div>
          <Badge
            variant={job.status === 'completed' ? 'success' : job.status === 'failed' ? 'error' : 'processing'}
          >
            {job.status}
          </Badge>
        </div>
      ))}
    </div>
  );
}

export default CrawlHistory;
