#!/usr/bin/env bash
set -e
for kb in bangla_phonetic bangla_fixed; do
  echo "==> building $kb"
  (cd "$kb" && kmc build)
done
echo "Done. Installable packages:"
ls -1 */build/*.kmp
