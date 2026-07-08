import CitationCard from './CitationCard';

/**
 * Single chat message bubble.
 * User messages are right-aligned, AI messages are left-aligned with citations.
 */
function ChatMessage({ message }) {
  const { role, content, citations = [] } = message;
  const isUser = role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-slide-up`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-brand-600 text-white rounded-br-md'
            : 'bg-surface-800 text-surface-200 rounded-bl-md border border-surface-700'
        }`}
      >
        {/* Message avatar label */}
        <p className={`text-xs font-medium mb-1 ${isUser ? 'text-brand-200' : 'text-brand-400'}`}>
          {isUser ? 'You' : 'AI Assistant'}
        </p>

        {/* Message content */}
        <p className="text-sm leading-relaxed whitespace-pre-wrap">{content}</p>

        {/* Citations (AI messages only) */}
        {!isUser && citations.length > 0 && (
          <div className="mt-3 space-y-2">
            <p className="text-xs font-medium text-surface-400">Sources:</p>
            {citations.map((citation, idx) => (
              <CitationCard key={idx} citation={citation} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatMessage;
