# ===============================
# DIIaC Backend - Production Image
# Node 20 + Bullseye + PowerShell
# ===============================

FROM node:20-bullseye

# -----------------------------
# Inject deterministic build hash
# MUST appear immediately after FROM
# -----------------------------
ARG GOVERNANCE_BUILD_HASH
ENV GOVERNANCE_BUILD_HASH=${GOVERNANCE_BUILD_HASH}

# -----------------------------
# Install base system dependencies
# -----------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      ca-certificates \
      gnupg \
      pandoc \
      apt-transport-https && \
    rm -rf /var/lib/apt/lists/*

# -----------------------------
# Install PowerShell (robust + retry-safe)
# -----------------------------
RUN set -eux; \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg; \
    echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-debian-bullseye-prod bullseye main" > /etc/apt/sources.list.d/microsoft.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends --fix-missing powershell; \
    rm -rf /var/lib/apt/lists/*

# -----------------------------
# Application Setup
# -----------------------------
WORKDIR /workspace/backend-ui-bridge

COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY . .

EXPOSE 3001

CMD ["node", "server.js"]
