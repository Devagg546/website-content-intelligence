import { useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import EmptyState from '../common/EmptyState';

/**
 * Chat message area — displays conversation messages.
 * Auto-scrolls to the latest message.
 */
function ChatWindow({ messages = [] }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <EmptyState
        icon="💬"
        title="Ask anything about the website"
        description="Type a question below to get AI-powered answers with source citations from the crawled content."
        className="h-full"
      />
    );
  }

  return (
    <div className="flex-1 overflow-y-auto space-y-4 p-4">
      {messages.map((msg, index) => (
        <ChatMessage key={index} message={msg} />
      ))}
      <div ref={bottomRef} />
    </div>
  );
}

export default ChatWindow;
