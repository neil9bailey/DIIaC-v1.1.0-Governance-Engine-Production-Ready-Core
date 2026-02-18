import { useEffect, useState } from "react";
import { fetchTrustDashboard } from "./api";

interface Props {
  role: string;
}

export default function TrustDashboard({ role }: Props) {

  const [data, setData] = useState<any>(null);
  const [status, setStatus] = useState<string>("");

  useEffect(() => {
    if (role !== "admin") return;

    async function load() {
      try {
        setStatus("Loading trust state...");
        setData(null);

        const res = await fetchTrustDashboard();

        setData(res);
        setStatus("Trust state loaded.");
      } catch (err) {
        console.error(err);
        setStatus("Failed to load trust state.");
      }
    }

    load();
  }, [role]);

  if (role !== "admin") return null;

  return (
    <div className="panel">
      <h2>Trust Dashboard</h2>

      {status && (
        <div className="console-box">
          {status}
        </div>
      )}

      {data && (
        <div className="console-box">
          <div>
            <strong>Ledger Valid:</strong>{" "}
            {data.valid ? "Yes" : "No"}
          </div>

          <div>
            <strong>Record Count:</strong>{" "}
            {data.records}
          </div>

          <div>
            <strong>Ledger Root:</strong>{" "}
            {data.ledger_root}
          </div>

          <div>
            <strong>Frozen:</strong>{" "}
            {data.frozen ? "Yes" : "No"}
          </div>
        </div>
      )}
    </div>
  );
}
