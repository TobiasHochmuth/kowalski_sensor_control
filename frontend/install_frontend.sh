#!/usr/bin/env bash
set -e

[[ $EUID != 0 ]] && echo "Script must run as root." && exit 1

apt update
apt -y install nodejs npm

# Optional: install frontend dependencies
if [[ -d "frontend" && -f "frontend/package.json" ]]; then
  cd frontend
  npm install
  echo "Frontend ready. Run: npm run dev"
else
  echo "No ./frontend/package.json found. Run this from the repo root."
fi

rm -rf /var/lib/apt/lists/*
