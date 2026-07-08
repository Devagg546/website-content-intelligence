/**
 * Topic cloud — visual representation of identified topics.
 */
function TopicCloud({ topics = [] }) {
  if (topics.length === 0) {
    return (
      <p className="text-sm text-surface-500 text-center py-8">
        No topics identified yet. Crawl a website first.
      </p>
    );
  }

  // Calculate relative sizes based on page count
  const maxCount = Math.max(...topics.map((t) => t.page_count || 1));

  return (
    <div className="flex flex-wrap gap-2 justify-center">
      {topics.map((topic, idx) => {
        const ratio = (topic.page_count || 1) / maxCount;
        const fontSize = 0.75 + ratio * 0.75; // 0.75rem to 1.5rem

        return (
          <span
            key={idx}
            className="px-3 py-1.5 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-300 hover:bg-brand-500/20 transition-colors cursor-default"
            style={{ fontSize: `${fontSize}rem` }}
            title={`${topic.page_count} pages`}
          >
            {topic.name}
          </span>
        );
      })}
    </div>
  );
}

export default TopicCloud;
