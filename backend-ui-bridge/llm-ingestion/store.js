import fs from "fs";
import path from "path";

const STORE_DIR = "/workspace/artefacts/llm-ingestion";

export function appendRecord(record) {
  if (!fs.existsSync(STORE_DIR)) {
    fs.mkdirSync(STORE_DIR, { recursive: true });
  }

  const filename = `${Date.now()}-${record.response_hash}.json`;
  const fullPath = path.join(STORE_DIR, filename);

  const envelope = {
    timestamp: new Date().toISOString(),
    trusted: false,
    ...record
  };

  fs.writeFileSync(fullPath, JSON.stringify(envelope, null, 2));
}
