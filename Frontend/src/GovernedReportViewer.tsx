import { useEffect, useState } from "react";
import { listGovernedReports, exportDecisionPack } from "./api";

interface Props {
  role: string;
  executionId: string | null;
}

export default function GovernedReportViewer({ role, executionId }: Props) {

  const [reports, setReports] = useState<string[]>([]);

  async function refresh() {
    if (!executionId) return;

    try {
      const data = await listGovernedReports(executionId);
      setReports(data);
    } catch (err) {
      console.error(err);
    }
  }

  async function exportLatest() {
    if (!executionId) return;
    await exportDecisionPack(executionId);
  }

  useEffect(() => {
    refresh();
  }, [executionId]);

  if (!executionId) return null;

  return (
    <div className="panel">

      <h3>Governed Reports</h3>

      <button onClick={refresh}>
        Refresh
      </button>

      <button onClick={exportLatest}>
        Export Latest Decision Pack
      </button>

      <ul>
        {reports.map((file) => (
          <li key={file}>
            <a
              href={`http://localhost:3001/executions/${executionId}/reports/${file}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              {file}
            </a>
          </li>
        ))}
      </ul>

    </div>
  );
}
