#!/usr/bin/env bash
# Privacy-gated build wrapper.
# Runs the privacy check first; builds only if the check passes.
# Usage:  ./scripts/safe_build.sh           # build
#         ./scripts/safe_build.sh --serve   # build + local dev server

set -e
cd "$(dirname "$0")/.."

echo "🔒 Running privacy check..."
python3 scripts/privacy_check.py --strict

echo ""
echo "🏗  Privacy check passed. Building site..."
npx quartz build "$@"
