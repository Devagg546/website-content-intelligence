import { useState } from 'react';
import Card from '../components/common/Card';
import SearchBar from '../components/search/SearchBar';
import SearchResults from '../components/search/SearchResults';
import searchApi from '../api/searchApi';

/**
 * Search Page — /search
 * Google-like content search with keyword, semantic, and hybrid modes.
 */
function SearchPage() {
  const [results, setResults] = useState([]);
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async ({ query: searchQuery, searchType }) => {
    setQuery(searchQuery);
    setIsLoading(true);
    try {
      const response = await searchApi.search(searchQuery, searchType);
      setResults(response.results || []);
    } catch (error) {
      console.error('Search failed:', error);
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <Card.Header
          title="Content Search"
          subtitle="Search crawled website content using keyword, semantic, or hybrid search"
        />
        <SearchBar onSearch={handleSearch} isLoading={isLoading} />
      </Card>

      <Card>
        <SearchResults results={results} query={query} />
      </Card>
    </div>
  );
}

export default SearchPage;
