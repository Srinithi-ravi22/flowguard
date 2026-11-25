
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";

const COLORS = ["#22c55e", "#f59e0b", "#ef4444", "#991b1b"];

function Charts({ results = [] }) {
  // Count executions by risk severity
  const riskData = ["LOW", "MEDIUM", "HIGH", "CRITICAL"].map(
    (severity) => ({
      name: severity,
      value: results.filter(
        (item) => item.severity?.toUpperCase() === severity
      ).length,
    })
  );

  // Calculate total events for each workflow
  const workflowMap = {};

  results.forEach((item) => {
    const workflow = item.workflow_name || "Unknown";

    workflowMap[workflow] =
      (workflowMap[workflow] || 0) + (item.total_events || 0);
  });

  const executionData = Object.entries(workflowMap).map(
    ([workflow, events]) => ({
      workflow,
      events,
    })
  );

  return (
    <div className="charts-grid">
      <div className="chart-card">
        <h3>Risk Distribution</h3>

        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={riskData}
              dataKey="value"
              nameKey="name"
              outerRadius={90}
              label
            >
              {riskData.map((entry, index) => (
                <Cell key={entry.name} fill={COLORS[index]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-card">
        <h3>Workflow Event Activity</h3>

        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={executionData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="workflow" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar
              dataKey="events"
              name="Total Events"
              fill="#2563eb"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default Charts;
