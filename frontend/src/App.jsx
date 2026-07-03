import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import CrawlPage from './pages/CrawlPage';
import AskAIPage from './pages/AskAIPage';
import SearchPage from './pages/SearchPage';
import DashboardPage from './pages/DashboardPage';
import GapsPage from './pages/GapsPage';
import InsightsPage from './pages/InsightsPage';
import NotFoundPage from './pages/NotFoundPage';

/**
 * Root application component with route definitions.
 * All routes are wrapped in the Layout component for consistent navigation.
 */
function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        {/* Default redirect to crawl page */}
        <Route index element={<Navigate to="/crawl" replace />} />

        {/* Main feature pages */}
        <Route path="crawl" element={<CrawlPage />} />
        <Route path="ask" element={<AskAIPage />} />
        <Route path="search" element={<SearchPage />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="gaps" element={<GapsPage />} />
        <Route path="insights" element={<InsightsPage />} />

        {/* 404 */}
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}

export default App;
