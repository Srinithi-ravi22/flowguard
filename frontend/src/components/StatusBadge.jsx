import "../styles/status.css";

function StatusBadge({ status }) {
  const value = status.toLowerCase().replace(/\s+/g, "-");

  return (
    <span className={`status-badge ${value}`}>
      {status}
    </span>
  );
}

export default StatusBadge;