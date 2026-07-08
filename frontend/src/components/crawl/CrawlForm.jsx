import { useState } from 'react';
import Button from '../common/Button';
import Input from '../common/Input';

/**
 * Crawl form — URL input with start button and max pages configuration.
 */
function CrawlForm({ onSubmit, isLoading = false }) {
  const [url, setUrl] = useState('');
  const [maxPages, setMaxPages] = useState(500);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim()) {
      onSubmit({ url: url.trim(), maxPages });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        id="crawl-url"
        label="Website URL"
        type="url"
        placeholder="https://www.example.com"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        required
      />

      <Input
        id="max-pages"
        label="Max Pages"
        type="number"
        min={1}
        max={500}
        value={maxPages}
        onChange={(e) => setMaxPages(parseInt(e.target.value) || 500)}
      />

      <Button
        type="submit"
        variant="primary"
        size="lg"
        loading={isLoading}
        disabled={!url.trim()}
        className="w-full"
      >
        {isLoading ? 'Starting Crawl...' : '🕷️ Start Crawling'}
      </Button>
    </form>
  );
}

export default CrawlForm;
