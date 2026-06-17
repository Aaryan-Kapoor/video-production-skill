#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL="$ROOT/skills/video-production"
DIST="$ROOT/dist"
rm -rf "$DIST"
mkdir -p "$DIST"
python3 - "$SKILL" <<'PY'
from pathlib import Path
import re, sys
skill = Path(sys.argv[1])
text = (skill / 'SKILL.md').read_text(encoding='utf-8')
if not text.startswith('---'):
    raise SystemExit('SKILL.md must start with YAML frontmatter')
parts = text.split('---', 2)
fm = parts[1]
name = re.search(r'^name:\s*([a-z0-9-]+)\s*$', fm, re.M)
desc = re.search(r'^description:\s*(.+)$', fm, re.M)
if not name or name.group(1) != skill.name:
    raise SystemExit('frontmatter name must match folder name')
if not desc or len(desc.group(1).strip()) < 20:
    raise SystemExit('description is missing or too short')
print('Validation OK')
PY
find "$SKILL" -type d -name __pycache__ -prune -exec rm -rf {} +
(cd "$ROOT/skills" && zip -qr "$DIST/video-production.zip" video-production)
cp "$DIST/video-production.zip" "$DIST/video-production.skill"
python3 - "$DIST" <<'PY'
from pathlib import Path
import sys, zipfile
for p in Path(sys.argv[1]).glob('video-production.*'):
    with zipfile.ZipFile(p) as z:
        assert 'video-production/SKILL.md' in z.namelist()
    print(f'Packaged {p}')
PY
