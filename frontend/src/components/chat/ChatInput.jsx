import { useState } from 'react';
import Button from '../common/Button';

/**
 * Chat input bar — question input with send button.
 */
function ChatInput({ onSend, isLoading = false }) {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim() && !isLoading) {
      onSend(question.trim());
      setQuestion('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-end gap-3 p-4 border-t border-surface-700">
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask a question about the website content..."
        rows={1}
        className="input-field resize-none flex-1"
        disabled={isLoading}
      />
      <Button
        type="submit"
        variant="primary"
        loading={isLoading}
        disabled={!question.trim()}
      >
        Send
      </Button>
    </form>
  );
}

export default ChatInput;
