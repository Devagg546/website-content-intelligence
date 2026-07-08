import { useState, useEffect } from 'react';
import Card from '../components/common/Card';
import Spinner from '../components/common/Spinner';
import TopicCloud from '../components/insights/TopicCloud';
import DistributionChart from '../components/insights/DistributionChart';
import EntityList from '../components/insights/EntityList';
import insightsApi from '../api/insightsApi';

/**
 * Insights Page — /insights
 * AI-generated content intelligence with topics, distribution, and entities.
 */
function InsightsPage() {
  const [insights, setInsights] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadInsights();
  }, []);

  const loadInsights = async () => {
    setIsLoading(true);
    try {
      const data = await insightsApi.getInsights();
      setInsights(data);
    } catch (error) {
      console.error('Failed to load insights:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Spinner size="lg" label="Generating insights..." className="py-20" />;
  }

  return (
    <div className="space-y-6">
      {/* Topics */}
      <Card>
        <Card.Header
          title="Topics Covered"
          subtitle="Main topics identified across the website"
        />
        <TopicCloud topics={insights?.topics || []} />
      </Card>

      {/* Content Distribution */}
      <Card>
        <Card.Header
          title="Content Distribution"
          subtitle="How content is distributed across topics"
        />
        <DistributionChart data={insights?.content_distribution || []} />
      </Card>

      {/* Frequently Mentioned Entities */}
      <Card>
        <Card.Header
          title="Frequently Mentioned Entities"
          subtitle="Brands, locations, services, and products found in content"
        />
        <EntityList entities={insights?.frequent_entities || {}} />
      </Card>
    </div>
  );
}

export default InsightsPage;
