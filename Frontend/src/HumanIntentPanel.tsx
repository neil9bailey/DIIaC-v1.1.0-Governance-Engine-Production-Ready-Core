import { useEffect, useState } from "react";
import {
  createHumanInput,
  listHumanInputs
} from "./api";

export default function HumanIntentPanel() {
  const [role, setRole] = useState("CTO");
  const [subject, setSubject] = useState("");
  const [requirements, setRequirements] = useState("");
  const [inputs, setInputs] = useState<string[]>([]);

  async function refresh() {
    const data = await listHumanInputs();
    setInputs(data);
  }

  async function handleSubmit() {
    if (!subject || !requirements) return;

    await createHumanInput({
      role,
      subject,
      requirements
    });

    setSubject("");
    setRequirements("");
    await refresh();
  }

  useEffect(() => {
    refresh();
  }, []);

  return (
    <div className="panel">
      <h2>Strategic Requirement Intake</h2>

      <div className="input-grid">
        <input
          value={role}
          onChange={(e) => setRole(e.target.value)}
          placeholder="Role (e.g. CTO)"
          className="input-dark"
        />

        <input
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          placeholder="Subject"
          className="input-dark"
        />
      </div>

      <textarea
        value={requirements}
        onChange={(e) => setRequirements(e.target.value)}
        placeholder="Enter structured requirements..."
        className="textarea-console"
      />

      <button className="btn-primary" onClick={handleSubmit}>
        Save Strategic Requirement
      </button>

      <div className="console-box">
        <h4>Saved Requirements</h4>
        {inputs.map((f) => (
          <div key={f}>{f}</div>
        ))}
      </div>
    </div>
  );
}
