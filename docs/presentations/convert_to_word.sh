#!/bin/bash
# Converts whitepaper.md to whitepaper.docx
# Renders mermaid diagrams to PNG images first, then runs pandoc

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT="$SCRIPT_DIR/whitepaper.md"
OUTPUT="$SCRIPT_DIR/whitepaper.docx"
IMG_DIR="$SCRIPT_DIR/whitepaper_images"
WORKING="$SCRIPT_DIR/.whitepaper_converted.md"

echo "→ Rendering mermaid diagrams..."
python3 "$SCRIPT_DIR/render_mermaid.py" "$INPUT" "$WORKING" "$IMG_DIR"

echo "→ Converting to Word..."
pandoc "$WORKING" \
    -o "$OUTPUT" \
    --from markdown \
    --to docx \
    --highlight-style tango

rm -f "$WORKING"

echo "✓ Done: $OUTPUT"
