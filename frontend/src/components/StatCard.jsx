import "../styles/dashboard.css";

function StatCard({ title, value, color }) {
  return (
    <div className="stat-card">
      <div
        className="stat-indicator"
        style={{ backgroundColor: color }}
      ></div>

      <div>
        <h4>{title}</h4>
        <h2>{value}</h2>
      </div>
    </div>
  );
}

export default StatCard;