#!/bin/bash
# Build wrapper for the iohanngrig.github.io site.
#
# Runs the standard Quartz build, then applies two post-build fixes:
#
#   1. Reposition the legacy 2019 archive from /static/legacy/ to /legacy/.
#   2. Add the .html extension to extensionless HTML files Quartz emits
#      under public/lectures/. Quartz strips the .html suffix when copying
#      Quarto-rendered chapters from content/, leaving the file at a path
#      with no extension. GitHub Pages serves those as application/octet-stream
#      (browsers treat them as downloads), so we restore the extension.
#      GitHub Pages' pretty-URL fallback still resolves /foo -> /foo.html,
#      so the index links keep working without modification.
#
# Use this script — or `npm run build` — instead of `npx quartz build` for
# any local build, CI build, or pre-deploy verification.

set -euo pipefail

# Run Quartz build (forward any args, e.g. --serve, --bundleInfo)
npx quartz build "$@"

# Fix 1: Reposition the legacy archive to its public URL
if [ -d public/static/legacy ]; then
  rm -rf public/legacy
  mv public/static/legacy public/legacy
  echo "Repositioned legacy archive: public/static/legacy -> public/legacy"
fi

# Fix 2: Restore .html extension on Quarto-rendered chapters under public/lectures/
fixed=0
if [ -d public/lectures ]; then
  while IFS= read -r f; do
    if file "$f" 2>/dev/null | grep -q "HTML document"; then
      mv "$f" "${f}.html"
      fixed=$((fixed + 1))
    fi
  done < <(find public/lectures -type f ! -name "*.*")
  if [ "$fixed" -gt 0 ]; then
    echo "Restored .html extension on $fixed Quarto-rendered chapter file(s)"
  fi
fi

