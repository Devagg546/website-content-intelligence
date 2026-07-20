import { useState } from 'react';
import Button from '../common/Button';
import Input from '../common/Input';

/**
 * Crawl form — URL input with start button and max pages configuration.
 */
function CrawlForm({ onSubmit, isLoading = false }) {
  const [url, setUrl] = useState('');
  const [maxPages, setMaxPages] = useState(500);

  const parsedMaxPages = parseInt(maxPages);
  const isMaxPagesInvalid = maxPages === '' || isNaN(parsedMaxPages) || parsedMaxPages <= 0;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim() && !isMaxPagesInvalid) {
      onSubmit({ url: url.trim(), maxPages: parsedMaxPages });
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

      <div>
        <Input
          id="max-pages"
          label="Max Pages"
          type="number"
          min={0}
          value={maxPages}
          onChange={(e) => setMaxPages(e.target.value)}
        />
        {maxPages !== '' && parsedMaxPages === 0 && (
          <p style={{ color: '#f87171', fontSize: '0.85rem', marginTop: '0.35rem' }}>
            Enter number greater than 0.
          </p>
        )}
      </div>

      <Button
        type="submit"
        variant="primary"
        size="lg"
        loading={isLoading}
        disabled={!url.trim() || isMaxPagesInvalid}
        className="w-full"
      >
        {isLoading ? 'Starting Crawl...' : '🕷️ Start Crawling'}
      </Button>
    </form>
  );
}

export default CrawlForm;
