import { useLocation } from 'react-router-dom';

/**
 * Page title mapping from route paths.
 */
const pageTitles = {
  '/crawl': 'Crawl Website',
  '/ask': 'Ask AI',
  '/search': 'Content Search',
  '/dashboard': 'Dashboard',
  '/gaps': 'Content Gaps',
  '/insights': 'AI Insights',
};

/**
 * Header bar component.
 * Shows current page title and optional status indicators.
 */
function Header() {
  const location = useLocation();
  const title = pageTitles[location.pathname] || 'Content Intelligence';

  return (
    <header className="sticky top-0 z-20 bg-surface-950/80 backdrop-blur-xl border-b border-surface-800">
      <div className="flex items-center justify-between px-8 py-4">
        <div>
          <h2 className="text-xl font-semibold text-surface-100">{title}</h2>
        </div>

        <div className="flex items-center gap-4">
          {/* Status indicator */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface-800/60 border border-surface-700">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse-slow" />
            <span className="text-xs text-surface-400">System Online</span>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
