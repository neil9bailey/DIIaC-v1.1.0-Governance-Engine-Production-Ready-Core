import { useState } from "react";
import { runGovernanceDecision } from "./api";

interface Props {
  role: string;
  onExecutionComplete: (executionId: string) => void;
}

export default function GovernedCtoStrategy({ role, onExecutionComplete }: Props) {

  const [reasoningLevel, setReasoningLevel] = useState("R2");
  const [policyLevel, setPolicyLevel] = useState("P1");
  const [status, setStatus] = useState("");
  const [executionId, setExecutionId] = useState<string | null>(null);
  const [packHash, setPackHash] = useState<string | null>(null);
  const [ledgerRoot, setLedgerRoot] = useState<string | null>(null);

  async function execute(provider: string) {

    try {
      setStatus("Executing governance contract...");

      const response = await runGovernanceDecision({
        provider,
        reasoning_level: reasoningLevel,
        policy_level: policyLevel
      });

      const state = response.execution_state;

      setExecutionId(state.execution_id);
      setPackHash(state.pack_hash);
      setLedgerRoot(state.ledger_root);

      onExecutionComplete(state.execution_id);

      setStatus("Governance execution complete.");

    } catch (err: any) {
      console.error(err);
      setStatus("Execution failed.");
    }
  }

  return (
    <div className="panel">

      <h2>Governed Decision Report Engine</h2>

      {role === "admin" && (
        <div style={{ marginBottom: "1rem" }}>

          <label>Reasoning Level:</label>
          <select
            value={reasoningLevel}
            onChange={(e) => setReasoningLevel(e.target.value)}
          >
            <option value="R0">R0 — Executive Only</option>
            <option value="R1">R1 — Structured</option>
            <option value="R2">R2 — Analytical</option>
            <option value="R3">R3 — Strategic</option>
            <option value="R4">R4 — Scenario</option>
            <option value="R5">R5 — Adversarial Deep</option>
          </select>

          <br /><br />

          <label>Policy Level:</label>
          <select
            value={policyLevel}
            onChange={(e) => setPolicyLevel(e.target.value)}
          >
            <option value="P0">P0 — Minimal</option>
            <option value="P1">P1 — Standard</option>
            <option value="P2">P2 — Enhanced</option>
            <option value="P3">P3 — Regulated</option>
            <option value="P4">P4 — High Assurance</option>
            <option value="P5">P5 — Critical Infrastructure</option>
          </select>

        </div>
      )}

      <div style={{ marginBottom: "1rem" }}>
        <button onClick={() => execute("ChatGPT")}>
          Execute via ChatGPT
        </button>
      </div>

      {status && <div className="status">{status}</div>}

      {executionId && (
        <div style={{ marginTop: "1rem" }}>
          <strong>Execution ID:</strong> {executionId}<br />
          <strong>Pack Hash:</strong> {packHash}<br />
          <strong>Ledger Root:</strong> {ledgerRoot}
        </div>
      )}

    </div>
  );
}
