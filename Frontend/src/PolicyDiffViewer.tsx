import { useState } from "react";
import { runPolicyDiff } from "./api";

export default function PolicyDiffViewer() {
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  async function run() {
    try {
      const r = await runPolicyDiff(
        "CTO_STRATEGY_BASELINE",
        "1.0.0",
        "1.1.0"
      );
      setResult(r);
      setError(null);
    } catch (e) {
      setError("Simulation failed");
    }
  }

  return (
    <section style={{ marginTop: "2rem" }}>
      <h3>Policy Version Diff & Simulation</h3>

      <p>
        This simulation shows what <strong>would change</strong> if a
        policy version were updated. No bindings, artefacts, or ledger
        entries are modified.
      </p>

      <button onClick={run}>
        Simulate Policy Change
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <>
          <h4>Structural Changes</h4>
          <ul>
            {result.diff.changes.map((c: any, i: number) => (
              <li key={i}>
                <strong>{c.field}</strong>
              </li>
            ))}
          </ul>

          <h4>Simulated Impact</h4>
          <pre>
{JSON.stringify(result.simulated_impact, null, 2)}
          </pre>
        </>
      )}
    </section>
  );
}
