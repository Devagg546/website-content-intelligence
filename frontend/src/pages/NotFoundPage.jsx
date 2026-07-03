import { Link } from 'react-router-dom';
import Button from '../components/common/Button';

/**
 * 404 Not Found page.
 */
function NotFoundPage() {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <div className="text-8xl font-bold gradient-text mb-4">404</div>
      <h2 className="text-2xl font-semibold text-surface-200 mb-2">Page Not Found</h2>
      <p className="text-surface-400 mb-8">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <Link to="/crawl">
        <Button variant="primary">Go to Dashboard</Button>
      </Link>
    </div>
  );
}

export default NotFoundPage;
