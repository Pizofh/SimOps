#!/bin/sh
set -eu

: "${SIMOPS_API_BASE_URL:=http://localhost:8000}"

cat <<EOF >/usr/share/nginx/html/config.js
window.__SIMOPS_CONFIG__ = {
  apiBaseUrl: "${SIMOPS_API_BASE_URL}"
};
EOF

