import { useState, useEffect } from "react";
import HumanInputPanel from "./HumanInputPanel";
import GovernedCtoStrategy from "./GovernedCtoStrategy";
import GovernedReportViewer from "./GovernedReportViewer";
import ImpactViewer from "./ImpactViewer";
import TrustDashboard from "./TrustDashboard";

export default function App() {

  const [role, setRole] = useState<string>(
    localStorage.getItem("role") || "customer"
  );

  const [latestExecutionId, setLatestExecutionId] = useState<string | null>(null);

  useEffect(() => {
    localStorage.setItem("role", role);
  }, [role]);

  return (
    <div className="app-container">

      <header className="enterprise-header">
        <div className="brand-left">
          <h1 className="brand-title">VendorLogic</h1>
          <span className="brand-product">
            DIIaC™ — Decision Intelligence Infrastructure as Code
          </span>
        </div>

        <div className="brand-right">
          <div className="customer-label">
            Customer: Customer X
          </div>

          <div className="role-toggle">
            <label>Mode:</label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
              <option value="customer">Customer</option>
              <option value="admin">Admin</option>
            </select>
          </div>
        </div>
      </header>

      <main className="main-content">

        <HumanInputPanel />

        <GovernedCtoStrategy
          role={role}
          onExecutionComplete={(executionId: string) =>
            setLatestExecutionId(executionId)
          }
        />

        <GovernedReportViewer
          role={role}
          executionId={latestExecutionId}
        />

        {role === "admin" && (
          <>
            <ImpactViewer role={role} />
            <TrustDashboard role={role} />
          </>
        )}

      </main>

      <footer className="enterprise-footer">
        © 2026 VendorLogic — DIIaC™ Platform
      </footer>

    </div>
  );
}
