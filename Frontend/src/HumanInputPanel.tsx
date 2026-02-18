import { useState } from "react";
import { createHumanInput } from "./api";

interface Props {
  onIntentSaved?: () => void;
}

export default function HumanInputPanel({ onIntentSaved }: Props) {

  const [text, setText] = useState("");
  const [status, setStatus] = useState("");
  const [saving, setSaving] = useState(false);

  async function submit() {

    if (!text.trim()) {
      setStatus("Input required.");
      return;
    }

    try {
      setSaving(true);
      setStatus("Saving intent...");

      await createHumanInput({
        raw_text: text.trim()
      });

      setStatus("✔ Intent saved successfully.");
      setText("");

      if (onIntentSaved) {
        onIntentSaved();
      }

    } catch (err: any) {
      console.error(err);
      setStatus("Error saving intent.");
    }

    setSaving(false);
  }

  return (
    <div className="panel">

      <h2>Human Intent</h2>

      <textarea
        rows={8}
        placeholder="Enter strategic objective or free-form board directive..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        style={{ width: "100%" }}
      />

      <button
        onClick={submit}
        disabled={saving}
      >
        Submit Intent
      </button>

      {status && (
        <div className="status">
          {status}
        </div>
      )}

    </div>
  );
}
