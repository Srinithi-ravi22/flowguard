
import { useEffect, useState } from "react";
import api from "../services/api";
import RiskBadge from "../components/RiskBadge";
import StatusBadge from "../components/StatusBadge";
import "../styles/table.css";

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/alerts")
      .then((response) => {
        setAlerts(response.data.alerts || []);
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load alerts.");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <h2>Loading alerts...</h2>;
  if (error) return <h2>{error}</h2>;

  return (
    <div className="table-page">
      <h1>Alerts ({alerts.length})</h1>

      <table className="data-table">
        <thead>
          <tr>
            <th>Alert ID</th>
            <th>Workflow</th>
            <th>Risk Score</th>
            <th>Severity</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {alerts.map((alert) => (
            <tr key={alert.alert_id}>
              <td>{alert.alert_id.slice(0, 8)}</td>
              <td>{alert.workflow_name}</td>
              <td>{alert.risk_score}</td>
              <td><RiskBadge level={alert.severity} /></td>
              <td><StatusBadge status={alert.status} /></td>
            </tr>
          ))}

          {alerts.length === 0 && (
            <tr><td colSpan="5">No alerts found</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Alerts;
