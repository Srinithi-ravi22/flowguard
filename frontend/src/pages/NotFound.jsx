import { Link } from "react-router-dom";

function NotFound() {
  return (
    <div
      style={{
        height: "100vh",
        display: "grid",
        placeItems: "center",
        background: "#0f172a",
        color: "#fff",
        textAlign: "center",
      }}
    >
      <div>
        <h1 style={{ fontSize: "72px", marginBottom: "10px" }}>404</h1>

        <p style={{ marginBottom: "20px" }}>
          The page you are looking for was not found.
        </p>

        <Link
          to="/"
          style={{
            color: "#60a5fa",
            textDecoration: "none",
            fontWeight: "bold",
          }}
        >
          ← Back to Dashboard
        </Link>
      </div>
    </div>
  );
}

export default NotFound;