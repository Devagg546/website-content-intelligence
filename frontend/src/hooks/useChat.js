import { useState, useCallback } from 'react';
import askApi from '../api/askApi';

/**
 * Custom hook for managing AI chat state.
 * Handles messages, sending questions, and loading state.
 */
export function useChat() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = useCallback(async (question) => {
    // Add user message
    const userMessage = { role: 'user', content: question };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await askApi.askQuestion(question);
      const aiMessage = {
        role: 'assistant',
        content: response.answer || 'No answer available.',
        citations: response.citations || [],
      };
      setMessages((prev) => [...prev, aiMessage]);
      return response;
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: `Error: ${error.message}`,
        citations: [],
      };
      setMessages((prev) => [...prev, errorMessage]);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  return {
    messages,
    isLoading,
    sendMessage,
    clearMessages,
  };
}

export default useChat;
