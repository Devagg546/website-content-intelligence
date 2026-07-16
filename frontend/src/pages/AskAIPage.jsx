import { useState } from 'react';
import ChatWindow from '../components/chat/ChatWindow';
import ChatInput from '../components/chat/ChatInput';
import askApi from '../api/askApi';
import { useAppContext } from '../context/AppContext';

function AskAIPage() {
  const { messages, setMessages } = useAppContext();
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (question) => {
    const userMessage = { role: 'user', content: question };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await askApi.askQuestion(question);
      const aiMessage = {
        role: 'assistant',
        content: response.answer || 'I could not find relevant information to answer your question.',
        citations: response.citations || [],
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: `Sorry, something went wrong: ${error.message}`,
        citations: [],
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)]">
      <div className="glass-card flex-1 flex flex-col overflow-hidden">
        <ChatWindow messages={messages} />
        <ChatInput onSend={handleSend} isLoading={isLoading} />
      </div>
    </div>
  );
}

export default AskAIPage;