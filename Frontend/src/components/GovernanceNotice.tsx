export default function GovernanceNotice() {
  return (
    <div
      style={{
        background: "#f5f7fa",
        borderLeft: "4px solid #3b82f6",
        padding: "0.75rem 1rem",
        marginBottom: "1rem",
        fontSize: "0.9rem"
      }}
    >
      <strong>Governance Notice</strong>
      <p style={{ margin: "0.25rem 0 0", color: "#374151" }}>
        AI-assisted content is treated as <strong>untrusted input</strong>.
        All outputs shown here are deterministically governed, policy-bound,
        and recorded in an immutable audit ledger.
      </p>
    </div>
  );
}
