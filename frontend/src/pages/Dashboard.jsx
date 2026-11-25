
import { useEffect, useState } from "react";
import api from "../services/api";
import StatCard from "../components/StatCard";
import Charts from "../components/Charts";
import RiskBadge from "../components/RiskBadge";
import StatusBadge from "../components/StatusBadge";
import "../styles/dashboard.css";

function Dashboard() {
  const [monitorData, setMonitorData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchMonitorData = async () => {
      try {
        const response = await api.get("/monitor");
        setMonitorData(response.data);
        setError("");
      } catch (err) {
        console.error("Dashboard API error:", err);
        setError("Unable to load FlowGuard monitoring data.");
      } finally {
        setLoading(false);
      }
    };

    fetchMonitorData();
  }, []);

  if (loading) return <h2>Loading FlowGuard data...</h2>;
  if (error) return <h2>{error}</h2>;

  const results = monitorData?.results || [];

  const alerts = results.filter(item => item.alert).length;

  const criticalRisk = results.filter(
    item => item.severity === "CRITICAL"
  ).length;

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>

      <p className="dashboard-subtitle">
        Workflow Monitoring & Protection Overview
      </p>

      <div className="stats-grid">
        <StatCard
          title="Total Workflows"
          value={monitorData.monitored_workflows}
          color="#2563eb"
        />

        <StatCard
          title="Executions"
          value={monitorData.monitored_executions}
          color="#10b981"
        />

        <StatCard
          title="Alerts"
          value={alerts}
          color="#f59e0b"
        />

        <StatCard
          title="Critical Risk"
          value={criticalRisk}
          color="#ef4444"
        />
      </div>

      <Charts results={monitorData.results || []} />

      <div className="dashboard-section">
        <h2>Recent Activity</h2>

        <table className="activity-table">
          <thead>
            <tr>
              <th>Workflow</th>
              <th>Status</th>
              <th>Risk</th>
            </tr>
          </thead>

          <tbody>
            {results.map((item) => (
              <tr key={item.execution_id}>
                <td>{item.workflow_name}</td>
                <td>
                  <StatusBadge
                    status={item.alert ? "Alert" : "Completed"}
                  />
                </td>
                <td>
                  <RiskBadge level={item.severity} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dashboard;
