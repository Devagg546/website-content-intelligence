import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import Footer from './Footer';

/**
 * Main layout wrapper.
 * Provides consistent structure: sidebar + header + content area + footer.
 * Uses React Router's <Outlet> to render the active page.
 */
function Layout() {
  return (
    <div className="flex min-h-screen bg-surface-950 text-surface-200">
      {/* Sidebar Navigation */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="flex-1 ml-64 flex flex-col min-h-screen">
        <Header />

        <main className="flex-1 p-8">
          <div className="animate-fade-in">
            <Outlet />
          </div>
        </main>

        <Footer />
      </div>
    </div>
  );
}

export default Layout;
