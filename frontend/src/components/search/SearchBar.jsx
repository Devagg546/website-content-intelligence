import { useState } from 'react';
import { HiOutlineMagnifyingGlass } from 'react-icons/hi2';

/**
 * Search bar with type selector (keyword, semantic, hybrid).
 */
function SearchBar({ onSearch, isLoading = false }) {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState('hybrid');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch({ query: query.trim(), searchType });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <div className="relative">
        <HiOutlineMagnifyingGlass className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-surface-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search website content..."
          className="input-field pl-12 pr-4"
          disabled={isLoading}
        />
      </div>

      <div className="flex items-center gap-2">
        {['hybrid', 'keyword', 'semantic'].map((type) => (
          <button
            key={type}
            type="button"
            onClick={() => setSearchType(type)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              searchType === type
                ? 'bg-brand-600 text-white'
                : 'bg-surface-800 text-surface-400 hover:text-surface-200'
            }`}
          >
            {type.charAt(0).toUpperCase() + type.slice(1)}
          </button>
        ))}
      </div>
    </form>
  );
}

export default SearchBar;
