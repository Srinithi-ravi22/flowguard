import "../styles/badges.css";

function RiskBadge({ level }) {
  const risk = level.toLowerCase();

  return (
    <span className={`risk-badge ${risk}`}>
      {level}
    </span>
  );
}

export default RiskBadge;