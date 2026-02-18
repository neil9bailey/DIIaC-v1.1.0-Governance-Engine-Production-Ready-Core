export type Role = "admin" | "viewer";

// 🔒 TEMPORARY — replaced later by real auth
export const CURRENT_ROLE: Role = "admin";

export function isAdmin(): boolean {
  return CURRENT_ROLE === "admin";
}

export function authHeaders(): HeadersInit {
  return {
    "x-role": CURRENT_ROLE
  };
}
