/**
 * Ask AI API — RAG-powered question answering.
 */
import apiClient from './client';

export const askApi = {
  /** Ask a natural language question */
  askQuestion: (question) =>
    apiClient.post('/ask', { question }),
};

export default askApi;
