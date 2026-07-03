import Badge from '../common/Badge';

/**
 * Real-time crawl progress display.
 * Shows pages crawled, status, and progress bar.
 */
function CrawlProgress({ status = {} }) {
  const { pages_crawled = 0, pages_total = 0, status: jobStatus = 'idle' } = status;
  const progress = pages_total > 0 ? (pages_crawled / pages_total) * 100 : 0;

  const statusVariant = {
    queued: 'info',
    in_progress: 'processing',
    completed: 'success',
    failed: 'error',
    idle: 'default',
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-surface-400">Progress</p>
          <p className="text-2xl font-bold text-surface-100">
            {pages_crawled}
            <span className="text-sm font-normal text-surface-500"> / {pages_total} pages</span>
          </p>
        </div>
        <Badge variant={statusVariant[jobStatus] || 'default'}>
          {jobStatus.replace('_', ' ').toUpperCase()}
        </Badge>
      </div>

      {/* Progress Bar */}
      <div className="w-full h-2 bg-surface-700 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-brand-500 to-brand-400 rounded-full transition-all duration-500 ease-out"
          style={{ width: `${Math.min(progress, 100)}%` }}
        />
      </div>
    </div>
  );
}

export default CrawlProgress;
