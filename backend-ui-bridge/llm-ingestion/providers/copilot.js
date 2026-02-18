import crypto from "crypto";

export async function ingestCopilot(prompt, parameters = {}) {
  const content = "Copilot response placeholder";

  return {
    provider: "copilot",
    model: parameters.model || "copilot-enterprise",
    prompt_hash: crypto.createHash("sha256").update(prompt).digest("hex"),
    response_hash: crypto.createHash("sha256").update(content).digest("hex"),
    content
  };
}
