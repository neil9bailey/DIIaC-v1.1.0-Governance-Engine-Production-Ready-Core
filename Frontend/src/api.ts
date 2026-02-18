const BASE = "http://localhost:3001";

type Role = "customer" | "admin";

function currentRole(): Role {
  const r = (localStorage.getItem("role") || "customer").toLowerCase();
  return r === "admin" ? "admin" : "customer";
}

async function request(path: string, options: RequestInit = {}) {
  const role = currentRole();

  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "x-role": role,
      ...(options.headers || {})
    }
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Request failed: ${res.status}`);
  }

  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) return res.json();
  return res.text();
}

/* =========================
   HUMAN INPUT
========================= */

export function createHumanInput(data: any) {
  return request("/api/human-input", {
    method: "POST",
    body: JSON.stringify(data)
  });
}

/* =========================
   GOVERNANCE EXECUTION
========================= */

export function runGovernanceDecision(provider: string) {
  return request("/govern/decision", {
    method: "POST",
    body: JSON.stringify({ provider })
  });
}

/* =========================
   EXECUTION REPORTS
========================= */

export function listGovernedReports(executionId: string) {
  return request(
    `/executions/${encodeURIComponent(executionId)}/reports`
  );
}

export async function downloadGovernedReport(
  executionId: string,
  file: string
) {
  const role = currentRole();

  const res = await fetch(
    `${BASE}/executions/${encodeURIComponent(
      executionId
    )}/reports/${encodeURIComponent(file)}`,
    {
      headers: { "x-role": role }
    }
  );

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "Download failed");
  }

  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = file;
  document.body.appendChild(a);
  a.click();
  a.remove();

  window.URL.revokeObjectURL(url);
}

/* =========================
   EXPORT DECISION PACK
========================= */

export async function exportDecisionPack(executionId: string) {
  const role = currentRole();

  const res = await fetch(
    `${BASE}/decision-pack/${encodeURIComponent(
      executionId
    )}/export`,
    {
      headers: { "x-role": role }
    }
  );

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "Export failed");
  }

  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = `decision-pack_${executionId}.zip`;
  document.body.appendChild(a);
  a.click();
  a.remove();

  window.URL.revokeObjectURL(url);
}

/* =========================
   TRUST (ADMIN)
========================= */

export function fetchTrustDashboard() {
  return request("/trust");
}

/* =========================
   POLICY IMPACT (ADMIN)
========================= */

export function runPolicyImpact() {
  return request("/api/impact/policy", {
    method: "POST"
  });
}
