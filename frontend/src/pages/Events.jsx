
import { useEffect, useState } from "react";
import api from "../services/api";
import "../styles/table.css";

function Events() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/events")
      .then((response) => {
        setEvents(response.data.events || []);
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load events.");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <h2>Loading events...</h2>;
  if (error) return <h2>{error}</h2>;

  return (
    <div className="table-page">
      <h1>Events ({events.length})</h1>

      <table className="data-table">
        <thead>
          <tr>
            <th>Workflow</th>
            <th>Event</th>
            <th>Execution ID</th>
            <th>Timestamp</th>
            <th>Source</th>
          </tr>
        </thead>

        <tbody>
          {events.map((event, index) => (
            <tr key={`${event.execution_id}-${index}`}>
              <td>{event.workflow_name}</td>
              <td>{event.event}</td>
              <td>{event.execution_id?.slice(0, 8)}</td>
              <td>
                {new Date(event.timestamp).toLocaleString()}
              </td>
              <td>{event.source}</td>
            </tr>
          ))}

          {events.length === 0 && (
            <tr>
              <td colSpan="5">No events found</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Events;
