/**
 * Search API — Content search endpoints.
 */
import apiClient from './client';

export const searchApi = {
  /** Search content by keyword, semantic, or hybrid */
  search: (query, searchType = 'hybrid', limit = 20) =>
    apiClient.post('/search', { query, search_type: searchType, limit }),
};

export default searchApi;
