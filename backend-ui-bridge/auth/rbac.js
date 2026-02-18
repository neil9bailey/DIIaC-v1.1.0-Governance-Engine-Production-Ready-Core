// backend-ui-bridge/auth/rbac.js
// ESM-compatible RBAC middleware for DIIaC

export function requireRole(allowedRoles = []) {
  return function (req, res, next) {
    const role =
      req.headers["x-role"] ||
      req.headers["X-Role"] ||
      req.headers["x-role".toLowerCase()];

    if (!role) {
      return res.status(403).json({
        error: "Forbidden",
        reason: "No role provided"
      });
    }

    if (!allowedRoles.includes(role)) {
      return res.status(403).json({
        error: "Forbidden",
        reason: "Insufficient role permissions"
      });
    }

    next();
  };
}
