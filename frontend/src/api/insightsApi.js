/**
 * Insights API — AI-generated content insights.
 */
import apiClient from './client';

export const insightsApi = {
  /** Get AI content insights */
  getInsights: () =>
    apiClient.get('/insights'),
};

export default insightsApi;
