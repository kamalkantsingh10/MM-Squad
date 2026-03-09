#!/usr/bin/env python3
"""
Extracts mermaid code blocks from a markdown file,
renders each to PNG via mmdc, and replaces the blocks
with image references in a new working markdown file.
"""

import re
import subprocess
import os
import sys
import tempfile

def main(input_file, working_file, img_dir):
    os.makedirs(img_dir, exist_ok=True)

    with open(input_file, "r") as f:
        content = f.read()

    pattern = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)
    matches = list(pattern.finditer(content))

    print(f"  Found {len(matches)} mermaid diagram(s)")

    new_content = content

    for i, m in enumerate(matches):
        img_name = f"diagram_{i+1}.png"
        img_path = os.path.join(img_dir, img_name)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False) as tmp:
            tmp.write(m.group(1))
            tmp_path = tmp.name

        result = subprocess.run(
            ["mmdc", "-i", tmp_path, "-o", img_path, "-b", "white", "--scale", "2"],
            capture_output=True, text=True
        )
        os.unlink(tmp_path)

        if result.returncode != 0:
            print(f"  WARNING: diagram {i+1} failed: {result.stderr.strip()}")
            continue

        print(f"  ✓ diagram {i+1} → {img_name}")

        rel_path = os.path.relpath(img_path, os.path.dirname(os.path.abspath(input_file)))
        new_content = new_content.replace(m.group(0), f"![]({rel_path})", 1)

    with open(working_file, "w") as f:
        f.write(new_content)

    print(f"  Working file written: {working_file}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
