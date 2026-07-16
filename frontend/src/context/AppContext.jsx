import { createContext, useContext, useState } from 'react';

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [activeCrawlJobId, setActiveCrawlJobId] = useState(null);
  const [systemStatus, setSystemStatus] = useState('online');
  const [lastCrawledUrl, setLastCrawledUrl] = useState('');
  const [crawlStatus, setCrawlStatus] = useState(null);
  const [messages, setMessages] = useState([]);

  const value = {
    activeCrawlJobId,
    setActiveCrawlJobId,
    systemStatus,
    setSystemStatus,
    lastCrawledUrl,
    setLastCrawledUrl,
    crawlStatus,
    setCrawlStatus,
    messages,
    setMessages,
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