#!/usr/bin/env bash
set -euo pipefail

LATEST_PRIVACY="$(ls -1t private_legal/privacy.private.*.html 2>/dev/null | head -n1 || true)"
LATEST_LEGAL="$(ls -1t private_legal/legal.private.*.html 2>/dev/null | head -n1 || true)"
LATEST_COOKIES="$(ls -1t private_legal/cookies.private.*.html 2>/dev/null | head -n1 || true)"

[ -n "$LATEST_PRIVACY" ] && cp "$LATEST_PRIVACY" frontend/public/privacy.html
[ -n "$LATEST_LEGAL" ] && cp "$LATEST_LEGAL" frontend/public/legal.html
[ -n "$LATEST_COOKIES" ] && cp "$LATEST_COOKIES" frontend/public/cookies.html

echo "Textos privados restaurados localmente."
