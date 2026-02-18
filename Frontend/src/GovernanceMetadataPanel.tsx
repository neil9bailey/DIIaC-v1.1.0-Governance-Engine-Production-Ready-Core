export interface GovernanceMetadata {
  contract_id?: string;
  contract_hash?: string;
  risk?: string;
}

/**
 * Safely extract metadata from governed markdown.
 * GUARANTEES string input.
 */
export function parseGovernanceMetadata(
  markdown: unknown
): GovernanceMetadata {
  if (typeof markdown !== "string") {
    console.error(
      "[parseGovernanceMetadata] Expected string, received:",
      markdown
    );
    return {};
  }

  const extract = (pattern: RegExp) => {
    const match = markdown.match(pattern);
    return match ? match[1].trim() : undefined;
  };

  return {
    contract_id: extract(/Contract ID:\s*(.+)/i),
    contract_hash: extract(/Contract Hash:\s*(.+)/i),
    risk: extract(/Risk Classification:\s*(.+)/i)
  };
}
