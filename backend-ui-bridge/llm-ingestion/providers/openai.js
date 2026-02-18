import crypto from "crypto";
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

export async function ingestOpenAI(prompt, parameters = {}) {
  const response = await client.chat.completions.create({
    model: parameters.model || "gpt-4o-mini",
    messages: [{ role: "user", content: prompt }],
    temperature: parameters.temperature ?? 0
  });

  const content = response.choices[0].message.content;

  return {
    provider: "openai",
    model: response.model,
    prompt_hash: crypto.createHash("sha256").update(prompt).digest("hex"),
    response_hash: crypto.createHash("sha256").update(content).digest("hex"),
    content
  };
}
