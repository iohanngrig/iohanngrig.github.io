#!/bin/bash
# Build wrapper for the iohanngrig.github.io site.
#
# Runs the standard Quartz build, then applies post-build fixes:
#
#   1. Reposition the legacy 2019 archive from /static/legacy/ to /legacy/.
#
#   2. Wrap Quarto-rendered chapter files into folder-with-index layout.
#      Quartz copies Quarto-rendered chapter files (e.g. <slug>.html)
#      together with their sibling Quarto asset directories (e.g.
#      <slug>_files/). GitHub Pages serves these files at the
#      extensionless URL with content-type "application/octet-stream"
#      (browsers download instead of render). Wrapping into
#      <slug>/index.html alongside <slug>/<slug>_files/ uses Pages'
#      native folder-with-index serving with text/html content-type.
#      Index page links of the form "/foo" auto-redirect to "/foo/"
#      (Pages' default behavior for directory paths), so existing
#      links keep working.
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

# Fix 2: First restore .html extension on extensionless HTML files Quartz
# emits (Quartz strips .html when copying .html source files), then wrap
# any chapter that has a sibling <slug>_files/ asset directory into the
# folder-with-index layout.
if [ -d public/lectures ]; then
  # Restore .html extension
  fixed_ext=0
  while IFS= read -r f; do
    if file "$f" 2>/dev/null | grep -q "HTML document"; then
      mv "$f" "${f}.html"
      fixed_ext=$((fixed_ext + 1))
    fi
  done < <(find public/lectures -type f ! -name "*.*")
  if [ "$fixed_ext" -gt 0 ]; then
    echo "Restored .html extension on $fixed_ext extensionless HTML file(s)"
  fi

  # Wrap Quarto chapters: <slug>.html + <slug>_files/ -> <slug>/index.html + <slug>/<slug>_files/
  wrapped=0
  while IFS= read -r files_dir; do
    base="${files_dir%_files}"
    chapter="${base}.html"
    if [ -f "$chapter" ]; then
      slug=$(basename "$base")
      target="${base}"
      mkdir -p "$target"
      mv "$chapter" "${target}/index.html"
      mv "$files_dir" "${target}/${slug}_files"
      wrapped=$((wrapped + 1))
    fi
  done < <(find public/lectures -maxdepth 4 -type d -name "*_files")
  if [ "$wrapped" -gt 0 ]; then
    echo "Wrapped $wrapped Quarto chapter(s) into folder-with-index layout"
  fi
fi
