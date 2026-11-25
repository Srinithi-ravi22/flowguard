
import { useEffect, useState } from "react";
import api from "../services/api";
import "../styles/table.css";

function Baselines() {
  const [baselines, setBaselines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/baselines")
      .then((response) => {
        const data = response.data || {};

        const formattedBaselines = Object.entries(data).map(
          ([workflow, config]) => ({
            workflow,
            expectedEvents: config.expected_events,
            maxRepetitions: config.max_repetitions,
            allowedRetries: config.allowed_retries,
          })
        );

        setBaselines(formattedBaselines);
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load workflow baselines.");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <h2>Loading baselines...</h2>;
  if (error) return <h2>{error}</h2>;

  return (
    <div className="table-page">
      <h1>Workflow Baselines ({baselines.length})</h1>

      <table className="data-table">
        <thead>
          <tr>
            <th>Workflow</th>
            <th>Expected Events</th>
            <th>Max Repetitions</th>
            <th>Allowed Retries</th>
          </tr>
        </thead>

        <tbody>
          {baselines.map((baseline) => (
            <tr key={baseline.workflow}>
              <td>{baseline.workflow}</td>
              <td>{baseline.expectedEvents}</td>
              <td>{baseline.maxRepetitions}</td>
              <td>{baseline.allowedRetries}</td>
            </tr>
          ))}

          {baselines.length === 0 && (
            <tr>
              <td colSpan="4">No baselines found</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Baselines;
