/**
 * Inventory API — Content inventory dashboard data.
 */
import apiClient from './client';

export const inventoryApi = {
  /** Get content inventory report */
  getInventory: () =>
    apiClient.get('/inventory'),

  /** Get paginated list of all pages */
  getPages: (page = 1, perPage = 20, search = '') =>
    apiClient.get('/pages', { params: { page, per_page: perPage, search: search || undefined } }),
};

export default inventoryApi;
