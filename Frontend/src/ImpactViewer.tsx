import { useState } from "react";
import { runPolicyImpact } from "./api";

interface Props {
  role: string;
}

export default function ImpactViewer({ role }: Props) {

  const [result, setResult] = useState<any>(null);
  const [status, setStatus] = useState<string>("");

  if (role !== "admin") return null;

  async function analyse() {
    try {
      setStatus("Running policy impact analysis...");
      setResult(null);

      const res = await runPolicyImpact();

      setResult(res);
      setStatus("Analysis complete.");
    } catch (err: any) {
      console.error(err);
      setStatus("Policy impact analysis failed.");
    }
  }

  return (
    <div className="panel">
      <h2>Policy Impact Analysis</h2>

      <div className="button-row">
        <button
          className="btn-primary"
          onClick={analyse}
        >
          Run Policy Impact
        </button>
      </div>

      {status && (
        <div className="console-box">
          {status}
        </div>
      )}

      {result && (
        <div className="console-box">
          <div><strong>Severity:</strong> {result.severity}</div>
          <div><strong>Impacted Controls:</strong> {result.impacted_controls}</div>
          <div><strong>Findings:</strong> {result.findings}</div>
          <div><strong>Evaluated At:</strong> {result.evaluated_at}</div>
        </div>
      )}
    </div>
  );
}
