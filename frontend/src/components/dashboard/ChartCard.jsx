import Card from '../common/Card';

/**
 * Chart card wrapper — provides consistent styling for chart containers.
 */
function ChartCard({ title, subtitle, children, className = '' }) {
  return (
    <Card className={className}>
      <Card.Header title={title} subtitle={subtitle} />
      <div className="h-64">
        {children}
      </div>
    </Card>
  );
}

export default ChartCard;
