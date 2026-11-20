#!/usr/bin/env bash
set -euo pipefail

registry=$1
version=$2
index_json="$RUNNER_TEMP/$registry.json"

# A newly published version may take time to appear across the public index.
curl --fail --silent --show-error --retry 15 --retry-delay 10 --retry-all-errors \
  --retry-max-time 160 --max-time 15 \
  "https://$registry/pypi/safety-gymnasium2/$version/json" --output "$index_json"

for artifact in dist/*.whl dist/*.tar.gz; do
  filename=${artifact##*/}
  digest=$(jq -er --arg filename "$filename" \
    '.urls[] | select(.filename == $filename and .yanked == false) | .digests.sha256' \
    "$index_json")
  printf '%s  %s\n' "$digest" "$artifact" | sha256sum --check -
done
