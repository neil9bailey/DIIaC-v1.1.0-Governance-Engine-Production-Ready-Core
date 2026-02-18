import { useState } from "react";
import ReactMarkdown from "react-markdown";
import {
  generateDerivedCompliance,
  listDerivedReports,
  fetchDerivedReport,
  exportDerivedReport
} from "./api";

export default function DerivedCompliancePanel() {
  const [files, setFiles] = useState<string[]>([]);
  const [content, setContent] = useState("");

  async function generate() {
    await generateDerivedCompliance();
    setFiles(await listDerivedReports());
  }

  return (
    <section>
      <h3>EU AI Act Compliance (Derived Evidence)</h3>

      <p>
        These artefacts are deterministically derived from execution metadata,
        governance contracts, and immutable ledger entries.
        No AI systems are involved in their generation.
      </p>

      <button onClick={generate}>
        Generate EU AI Act Compliance Reports
      </button>

      <ul>
        {files.map(f => (
          <li key={f}>
            <button onClick={async () => setContent(await fetchDerivedReport(f))}>
              {f}
            </button>{" "}
            <button onClick={() => exportDerivedReport(f, "docx")}>Word</button>{" "}
            <button onClick={() => exportDerivedReport(f, "pdf")}>PDF</button>
          </li>
        ))}
      </ul>

      {content && <ReactMarkdown>{content}</ReactMarkdown>}
    </section>
  );
}
