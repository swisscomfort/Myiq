#!/usr/bin/env bash
# Create new article skeleton from template
# Usage: ./wiki/scripts/new_article.sh "My New Title" author_name
set -euo pipefail

TITLE="${1:-New Article}"
AUTHOR="${2:-Unknown}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE="$ROOT/article_template.md"
SLUG="$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-|-$//g')"
OUT="$ROOT/$SLUG.md"
if [ -e "$OUT" ]; then
  echo "Article already exists: $OUT" >&2
  exit 1
fi

sed \
  -e "s/TITEL HIER/$TITLE/" \
  -e "s/2025-10-25/$(date +%F)/" \
  -e "s/author: \"Vorname Nachname\"/author: \"$AUTHOR\"/" \
  "$TEMPLATE" > "$OUT"

echo "Created new article: $OUT"