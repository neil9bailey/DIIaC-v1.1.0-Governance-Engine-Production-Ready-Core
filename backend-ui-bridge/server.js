import express from "express";
import cors from "cors";
import fs from "fs";
import path from "path";
import crypto from "crypto";
import archiver from "archiver";
import { fileURLToPath } from "url";
import OpenAI from "openai";
import { requireRole } from "./auth/rbac.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3001;

const WORKSPACE = "/workspace";
const HUMAN_INPUT_DIR = `${WORKSPACE}/artefacts/human-input`;
const DECISION_PACK_BASE = `${WORKSPACE}/artefacts/decision-packs`;
const LEDGER_PATH = `${WORKSPACE}/ledger/ledger.jsonl`;

const OPENAI_MODEL = process.env.OPENAI_MODEL || "gpt-4o-mini";
const LLM_ENABLED = process.env.LLM_INGESTION_ENABLED === "true";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

app.use(cors({
  origin: "http://localhost:5173",
  allowedHeaders: ["Content-Type", "x-role"]
}));

app.use(express.json());

/* ================= HASHING ================= */

function sha256(input) {
  return crypto.createHash("sha256").update(input).digest("hex");
}

/* ================= LEDGER ================= */

function ensureLedger() {
  if (!fs.existsSync(LEDGER_PATH)) fs.writeFileSync(LEDGER_PATH, "");
}

function getLastHash() {
  ensureLedger();
  const raw = fs.readFileSync(LEDGER_PATH, "utf8").trim();
  if (!raw) return "GENESIS";
  const lines = raw.split("\n").filter(Boolean);
  return JSON.parse(lines[lines.length - 1]).record_hash;
}

function appendLedger(record) {
  const full = { ...record, previous_hash: getLastHash() };
  const record_hash = sha256(JSON.stringify(full));
  const sealed = { ...full, record_hash };
  fs.appendFileSync(LEDGER_PATH, JSON.stringify(sealed) + "\n");
  return sealed;
}

/* ================= TRUST ================= */

app.get("/trust", requireRole(["admin"]), (_, res) => {
  ensureLedger();
  const raw = fs.readFileSync(LEDGER_PATH, "utf8").trim();
  const count = raw ? raw.split("\n").filter(Boolean).length : 0;

  res.json({
    valid: true,
    records: count,
    ledger_root: getLastHash(),
    frozen: false
  });
});

/* ================= HUMAN INPUT ================= */

app.post("/api/human-input",
  requireRole(["customer", "admin"]),
  (req, res) => {
    fs.mkdirSync(HUMAN_INPUT_DIR, { recursive: true });
    const id = Date.now();
    const filePath = path.join(HUMAN_INPUT_DIR, `${id}.json`);
    fs.writeFileSync(filePath, JSON.stringify(req.body, null, 2));
    res.json({ saved: `${id}.json` });
  }
);

/* ================= R/P ENFORCEMENT ================= */

function enforceSections(reportJSON, reasoning_level, policy_level) {

  const reasoningMap = {
    R0: ["executive_summary"],
    R1: ["executive_summary"],
    R2: ["executive_summary", "strategic_context"],
    R3: ["executive_summary", "strategic_context", "market_analysis"],
    R4: ["executive_summary", "strategic_context", "market_analysis", "risk_matrix"],
    R5: [
      "executive_summary",
      "strategic_context",
      "market_analysis",
      "risk_matrix",
      "financial_model",
      "scenario_analysis",
      "implementation_roadmap",
      "governance_implications",
      "vendor_scoring",
      "board_recommendation"
    ]
  };

  const policyMap = {
    P0: [],
    P1: [],
    P2: ["risk_matrix"],
    P3: ["regulatory_position"],
    P4: ["audit_trail"],
    P5: ["trace_manifest"]
  };

  const required = new Set([
    ...(reasoningMap[reasoning_level] || reasoningMap.R2),
    ...(policyMap[policy_level] || [])
  ]);

  const enforced = [];

  for (const section of required) {
    if (!reportJSON[section]) {
      reportJSON[section] = {
        enforced: true,
        note: `Section required by ${reasoning_level}/${policy_level} but not provided by AI`
      };
      enforced.push(section);
    }
  }

  return {
    report: reportJSON,
    enforced_sections: enforced
  };
}

/* ================= AI GENERATION ================= */

async function generateAI(context, reasoning_level, policy_level) {

  const reasoningMap = {
    R0: ["executive_summary"],
    R1: ["executive_summary"],
    R2: ["executive_summary", "strategic_context"],
    R3: ["executive_summary", "strategic_context", "market_analysis"],
    R4: ["executive_summary", "strategic_context", "market_analysis", "risk_matrix"],
    R5: [
      "executive_summary",
      "strategic_context",
      "market_analysis",
      "risk_matrix",
      "financial_model",
      "scenario_analysis",
      "implementation_roadmap",
      "governance_implications",
      "vendor_scoring",
      "board_recommendation"
    ]
  };

  const policyMap = {
    P0: [],
    P1: [],
    P2: ["risk_matrix"],
    P3: ["regulatory_position"],
    P4: ["audit_trail"],
    P5: ["trace_manifest"]
  };

  const requiredSections = Array.from(
    new Set([
      ...(reasoningMap[reasoning_level] || reasoningMap.R2),
      ...(policyMap[policy_level] || [])
    ])
  );

  const systemPrompt = `
You are an elite enterprise strategy AI operating under governance constraints.

Return STRICT JSON only.
The word JSON must appear in your output.

You MUST include these top-level sections at minimum:
${requiredSections.join(", ")}

Each section must be a structured JSON object.

You MAY include additional relevant sections if they improve clarity and depth.

Provide detailed, board-ready, professionally structured content.

Do NOT include markdown.
Do NOT include commentary.
Return a valid JSON object only.
`;

  const response = await openai.responses.create({
    model: OPENAI_MODEL,
    input: [
      { role: "system", content: systemPrompt },
      { role: "user", content: JSON.stringify(context) }
    ],
    text: { format: { type: "json_object" } }
  });

  const text = response.output_text;
  if (!text) throw new Error("AI returned empty response");

  return JSON.parse(text);
}

/* ================= POLICY IMPACT ================= */

app.post("/api/impact/policy",
  requireRole(["admin"]),
  (req, res) => {

    const { policy_level } = req.body;

    const severityMap = {
      P0: "LOW",
      P1: "LOW",
      P2: "MEDIUM",
      P3: "MEDIUM",
      P4: "HIGH",
      P5: "CRITICAL"
    };

    res.json({
      severity: severityMap[policy_level] || "LOW",
      impacted_controls: policy_level === "P0" ? 0 : 3,
      findings: 0,
      evaluated_at: new Date().toISOString()
    });
  }
);

/* ================= GOVERNED EXECUTION ================= */

app.post("/govern/decision",
  requireRole(["admin"]),
  async (req, res) => {

    try {

      let { provider, reasoning_level = "R2", policy_level = "P1" } = req.body;

      if (typeof provider === "object") {
        reasoning_level = provider.reasoning_level;
        policy_level = provider.policy_level;
        provider = provider.provider;
      }

      const executionId = crypto.randomUUID();

      const files = fs.readdirSync(HUMAN_INPUT_DIR)
        .filter(f => f.endsWith(".json"));

      if (!files.length)
        throw new Error("No human intent found");

      const latest = files.sort().reverse()[0];
      const contextRaw = fs.readFileSync(path.join(HUMAN_INPUT_DIR, latest), "utf8");
      const context = JSON.parse(contextRaw);
      const contextHash = sha256(contextRaw);

      const executionFolder = path.join(DECISION_PACK_BASE, executionId);
      const artefactsDir = path.join(executionFolder, "artefacts");
      fs.mkdirSync(artefactsDir, { recursive: true });

      const aiReport = LLM_ENABLED
        ? await generateAI(context, reasoning_level, policy_level)
        : {};

      const enforcement = enforceSections(
        aiReport,
        reasoning_level,
        policy_level
      );

      const decisionSummary = {
        execution_id: executionId,
        provider,
        reasoning_level,
        policy_level,
        governance_contract: "DIIaC_CORE_V1",
        generated_at: new Date().toISOString(),
        classification: "BOARD_READY",
        context_hash: contextHash,
        JSON: enforcement.report,
        __tier_enforcement: {
          reasoning_level,
          policy_level,
          enforced_sections: enforcement.enforced_sections,
          enforcement_timestamp: new Date().toISOString()
        }
      };

      fs.writeFileSync(
        path.join(artefactsDir, "decision_summary.json"),
        JSON.stringify(decisionSummary, null, 2)
      );

      if (reasoning_level === "R5") {
        fs.writeFileSync(
          path.join(artefactsDir, "strategy_report.json"),
          JSON.stringify(enforcement.report, null, 2)
        );
      }

      /* ===== DETERMINISTIC HASHING ===== */

      const artefactFiles = fs.readdirSync(artefactsDir).sort();

      const artefactHashes = artefactFiles.map(file => {
        const content = fs.readFileSync(path.join(artefactsDir, file), "utf8");
        return {
          name: file,
          hash: sha256(content)
        };
      });

      const initialPackHash = sha256(
        artefactHashes.map(a => a.hash).join("")
      );

      const manifest = {
        execution_id: executionId,
        governance_contract: "DIIaC_CORE_V1",
        reasoning_level,
        policy_level,
        context_hash: contextHash,
        artefacts: artefactHashes,
        pack_hash: initialPackHash,
        generated_at: new Date().toISOString()
      };

      fs.writeFileSync(
        path.join(artefactsDir, "governance_manifest.json"),
        JSON.stringify(manifest, null, 2)
      );

      const finalFiles = fs.readdirSync(artefactsDir).sort();
      const finalHashes = finalFiles.map(file => {
        const content = fs.readFileSync(path.join(artefactsDir, file), "utf8");
        return sha256(content);
      });

      const finalPackHash = sha256(finalHashes.join(""));

      const sealed = appendLedger({
        type: "GOVERNED_EXECUTION",
        execution_id: executionId,
        provider,
        reasoning_level,
        policy_level,
        context_hash: contextHash,
        pack_hash: finalPackHash,
        artefact_count: finalFiles.length,
        timestamp: new Date().toISOString()
      });

      res.json({
        execution_state: {
          execution_id: executionId,
          provider,
          reasoning_level,
          policy_level,
          pack_hash: finalPackHash,
          ledger_root: sealed.record_hash
        }
      });

    } catch (err) {
      console.error(err);
      res.status(500).json({ error: err.message });
    }
  }
);

/* ================= EXPORT ================= */

app.get("/decision-pack/:execution_id/export",
  requireRole(["admin"]),
  (req, res) => {

    const folder = path.join(
      DECISION_PACK_BASE,
      req.params.execution_id
    );

    if (!fs.existsSync(folder))
      return res.status(404).json({ error: "Not found" });

    res.setHeader(
      "Content-Disposition",
      `attachment; filename=decision-pack_${req.params.execution_id}.zip`
    );

    res.setHeader("Content-Type", "application/zip");

    const archive = archiver("zip");
    archive.pipe(res);
    archive.directory(folder, false);
    archive.finalize();
  }
);

app.listen(PORT, "0.0.0.0", () => {
  console.log("DIIaC Governance Engine — Deterministic R/P Enforcement Active");
});
