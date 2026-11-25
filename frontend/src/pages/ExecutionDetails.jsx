import { useParams } from "react-router-dom";

function ExecutionDetails() {
  const { id } = useParams();

  return (
    <div className="table-page">
      <h1>Execution Details</h1>

      <div
        style={{
          background: "#1e293b",
          padding: "20px",
          borderRadius: "12px",
          marginTop: "20px",
          color: "#fff",
        }}
      >
        <h2>Execution ID: {id}</h2>

        <p>
          <strong>Workflow:</strong> Payment Approval
        </p>

        <p>
          <strong>Status:</strong> Running
        </p>

        <p>
          <strong>Started:</strong> 10:30 AM
        </p>

        <p>
          <strong>Risk Score:</strong> 18%
        </p>

        <p>
          <strong>Protection:</strong> Safe
        </p>
      </div>
    </div>
  );
}

export default ExecutionDetails;