#!/bin/bash
# Build wrapper for the iohanngrig.github.io site.
#
# Runs the standard Quartz build, then repositions the legacy 2019 archive
# from /static/legacy/ (where Quartz's Static emitter places it) to /legacy/
# (the public-facing URL we want).
#
# Use this script — or `npm run build` — instead of `npx quartz build` for
# any local build, CI build, or pre-deploy verification.

set -euo pipefail

# Run Quartz build (forward any args, e.g. --serve, --bundleInfo)
npx quartz build "$@"

# Reposition the legacy archive to its public URL
if [ -d public/static/legacy ]; then
  rm -rf public/legacy
  mv public/static/legacy public/legacy
  echo "Repositioned legacy archive: public/static/legacy -> public/legacy"
fi
