#!/usr/bin/env bash
set -euo pipefail

# Ensure Node 20 if available in the environment
if command -v node >/dev/null 2>&1; then
  echo "Node version: $(node -v)"
fi

# Install dependencies with a clean, reproducible lockfile
npm ci

# Build using Node to avoid executable permission issues
npm run build
