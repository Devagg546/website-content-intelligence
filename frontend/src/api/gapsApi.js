/**
 * Gaps API — Content gap detection.
 */
import apiClient from './client';

export const gapsApi = {
  /** Get content gap report */
  getGaps: () =>
    apiClient.get('/gaps'),
};

export default gapsApi;
