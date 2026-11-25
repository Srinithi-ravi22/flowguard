
import { useEffect, useState } from "react";
import api from "../services/api";
import StatusBadge from "../components/StatusBadge";
import RiskBadge from "../components/RiskBadge";
import "../styles/table.css";

function Protection() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/monitor")
      .then((response) => {
        const results = response.data.results || [];

        const protectedResults = results.filter(
          (item) => item.alert || item.loop_detected
        );

        setResult(protectedResults);
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load protection analysis.");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <h2>Loading protection analysis...</h2>;
  if (error) return <h2>{error}</h2>;

  return (
    <div className="table-page">
      <h1>Protection</h1>
      <p>Detected workflows requiring protection attention.</p>

      <table className="data-table">
        <thead>
          <tr>
            <th>Workflow</th>
            <th>Risk Score</th>
            <th>Severity</th>
            <th>Loop Detected</th>
            <th>Protection Status</th>
          </tr>
        </thead>

        <tbody>
          {result.map((item, index) => (
            <tr key={`${item.execution_id}-${index}`}>
              <td>{item.workflow_name}</td>
              <td>{item.risk_score}</td>
              <td>
                <RiskBadge level={item.severity} />
              </td>
              <td>{item.loop_detected ? "Yes" : "No"}</td>
              <td>
                <StatusBadge status="Protected" />
              </td>
            </tr>
          ))}

          {result.length === 0 && (
            <tr>
              <td colSpan="5">No suspicious workflows detected</td>
            </tr>
          )}
        </tbody>
      </table>

      <p>
        <strong>Note:</strong> Protection is simulated. Excess executions
        are identified for suppression; external workflows are not
        actually blocked.
      </p>
    </div>
  );
}

export default Protection;
