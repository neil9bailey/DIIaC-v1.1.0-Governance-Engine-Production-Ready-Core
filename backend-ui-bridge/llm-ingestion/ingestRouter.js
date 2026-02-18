import express from "express";
import { ingestOpenAI } from "./providers/openai.js";
import { ingestCopilot } from "./providers/copilot.js";
import { appendRecord } from "./store.js";

export const ingestRouter = express.Router();

ingestRouter.post("/llm", async (req, res) => {
  if (process.env.LLM_INGESTION_ENABLED !== "true") {
    return res.status(403).json({ error: "LLM ingestion disabled" });
  }

  const { provider, prompt, parameters } = req.body;

  let record;

  if (provider === "openai") {
    record = await ingestOpenAI(prompt, parameters);
  } else if (provider === "copilot") {
    record = await ingestCopilot(prompt, parameters);
  } else {
    return res.status(400).json({ error: "Unknown provider" });
  }

  appendRecord(record);

  res.json({
    status: "captured",
    provider: record.provider,
    response_hash: record.response_hash
  });
});
