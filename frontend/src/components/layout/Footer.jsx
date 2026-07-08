/**
 * Footer component.
 * Simple footer with copyright and tech stack info.
 */
function Footer() {
  return (
    <footer className="px-8 py-4 border-t border-surface-800">
      <div className="flex items-center justify-between">
        <p className="text-xs text-surface-500">
          © {new Date().getFullYear()} Content Intelligence Assistant
        </p>
        <p className="text-xs text-surface-600">
          Built with React • FastAPI • ChromaDB • RAG
        </p>
      </div>
    </footer>
  );
}

export default Footer;
