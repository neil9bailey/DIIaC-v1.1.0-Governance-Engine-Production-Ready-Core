FROM node:20-bookworm

WORKDIR /workspace/backend-ui-bridge

# Install PowerShell
RUN apt-get update && \
    apt-get install -y wget apt-transport-https software-properties-common && \
    wget -q https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y powershell && \
    apt-get clean

# Copy package files
COPY backend-ui-bridge/package*.json ./
RUN npm install

# Copy backend source
COPY backend-ui-bridge .

# Expose port
EXPOSE 3001

CMD ["node", "server.js"]
