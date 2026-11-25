import { useState } from "react";
import SearchBar from "../components/SearchBar";
import StatusBadge from "../components/StatusBadge";
import "../styles/table.css";

const workflows = [
  {
    id: "WF-001",
    name: "Payment Approval",
    owner: "Finance",
    status: "Running",
  },
  {
    id: "WF-002",
    name: "Employee Onboarding",
    owner: "HR",
    status: "Completed",
  },
  {
    id: "WF-003",
    name: "Invoice Processing",
    owner: "Accounts",
    status: "Failed",
  },
  {
    id: "WF-004",
    name: "Leave Approval",
    owner: "HR",
    status: "Running",
  },
];

function Monitoring() {
  const [search, setSearch] = useState("");

  const filteredWorkflows = workflows.filter((workflow) =>
    workflow.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="table-page">
      <h1>Workflow Monitoring</h1>

      <SearchBar
        value={search}
        onChange={setSearch}
        placeholder="Search workflow..."
      />

      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Workflow</th>
            <th>Department</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {filteredWorkflows.map((workflow) => (
            <tr key={workflow.id}>
              <td>{workflow.id}</td>
              <td>{workflow.name}</td>
              <td>{workflow.owner}</td>
              <td>
                <StatusBadge status={workflow.status} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Monitoring;