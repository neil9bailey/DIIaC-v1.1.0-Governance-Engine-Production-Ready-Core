import { Router } from "express";
import crypto from "crypto";
import fs from "fs";
import path from "path";

const router = Router();

const BASE_DIR = "/workspace/artefacts/human-input";
const INPUT_DIR = path.join(BASE_DIR, "inputs");
const EXEC_DIR = path.join(BASE_DIR, "executions");

router.post("/human-input", (req, res) => {
  try {
    if (req.headers["x-role"] !== "admin") {
      return res.status(403).json({ error: "Admin role required" });
    }

    const { user_id, intent, policy_id, policy_version } = req.body;

    if (!user_id || !intent || !policy_id || !policy_version) {
      return res.status(400).json({ error: "Missing required fields" });
    }

    const timestamp = new Date().toISOString();
    const input_hash = crypto
      .createHash("sha256")
      .update(intent)
      .digest("hex");

    const input_id = `${Date.now()}-${input_hash.slice(0, 16)}`;

    const record = {
      schema_id: "diiac:human-input",
      schema_version: "1.0.0",
      input_id,
      input_hash,
      user_id,
      intent,
      policy_id,
      policy_version,
      timestamp
    };

    fs.writeFileSync(
      path.join(INPUT_DIR, `${input_id}.json`),
      JSON.stringify(record, null, 2)
    );

    fs.writeFileSync(
      path.join(EXEC_DIR, `${input_id}.json`),
      JSON.stringify(
        {
          input_id,
          policy_id,
          policy_version,
          timestamp,
          input_hash
        },
        null,
        2
      )
    );

    return res.json({
      status: "captured",
      input_id,
      input_hash
    });
  } catch (err: any) {
    return res.status(500).json({ error: err.message });
  }
});

export default router;
