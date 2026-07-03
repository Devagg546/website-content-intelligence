import { NavLink } from 'react-router-dom';
import {
  HiOutlineGlobeAlt,
  HiOutlineChatBubbleLeftRight,
  HiOutlineMagnifyingGlass,
  HiOutlineChartBarSquare,
  HiOutlineExclamationTriangle,
  HiOutlineLightBulb,
} from 'react-icons/hi2';

/**
 * Navigation items configuration.
 * Each item maps to a route and displays an icon + label.
 */
const navItems = [
  { path: '/crawl', label: 'Crawl Website', icon: HiOutlineGlobeAlt },
  { path: '/ask', label: 'Ask AI', icon: HiOutlineChatBubbleLeftRight },
  { path: '/search', label: 'Content Search', icon: HiOutlineMagnifyingGlass },
  { path: '/dashboard', label: 'Dashboard', icon: HiOutlineChartBarSquare },
  { path: '/gaps', label: 'Content Gaps', icon: HiOutlineExclamationTriangle },
  { path: '/insights', label: 'AI Insights', icon: HiOutlineLightBulb },
];

/**
 * Sidebar navigation component.
 * Displays the app logo and navigation links with active state indicators.
 */
function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-surface-900 border-r border-surface-800 flex flex-col z-30">
      {/* Logo */}
      <div className="p-6 border-b border-surface-800">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-brand-600 flex items-center justify-center">
            <span className="text-white font-bold text-lg">CI</span>
          </div>
          <div>
            <h1 className="text-sm font-bold text-surface-100 leading-tight">
              Content Intelligence
            </h1>
            <p className="text-xs text-surface-500">Assistant</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {navItems.map(({ path, label, icon: Icon }) => (
          <NavLink
            key={path}
            to={path}
            className={({ isActive }) =>
              isActive ? 'sidebar-link-active' : 'sidebar-link'
            }
          >
            <Icon className="w-5 h-5 flex-shrink-0" />
            <span className="text-sm font-medium">{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-surface-800">
        <p className="text-xs text-surface-500 text-center">
          v1.0.0 • RAG Platform
        </p>
      </div>
    </aside>
  );
}

export default Sidebar;
