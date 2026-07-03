import { createContext, useContext, useState } from 'react';

/**
 * Global application context.
 * Stores shared state like crawl status and system health.
 */
const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [activeCrawlJobId, setActiveCrawlJobId] = useState(null);
  const [systemStatus, setSystemStatus] = useState('online');
  const [lastCrawledUrl, setLastCrawledUrl] = useState('');

  const value = {
    // Crawl state
    activeCrawlJobId,
    setActiveCrawlJobId,

    // System status
    systemStatus,
    setSystemStatus,

    // Last crawled URL
    lastCrawledUrl,
    setLastCrawledUrl,
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
}

export default AppContext;
