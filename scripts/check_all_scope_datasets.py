from pathlib import Path
import re
import sys

datasets_js = Path("frontend/src/geo/datasets.js")
text = datasets_js.read_text()

single_paths = []
for match in re.finditer(r"municipiosPath\s*:\s*['\"]([^'\"]+_municipios\.geojson)['\"]", text):
    path = match.group(1)
    if path not in single_paths:
        single_paths.append(path)

starts = list(re.finditer(r"municipiosPaths\s*:\s*\[", text))
if not starts:
    print("ERROR: no encuentro municipiosPaths")
    sys.exit(1)

def find_matching_bracket(source, open_index):
    depth = 0
    quote = None
    escape = False

    for i in range(open_index, len(source)):
        ch = source[i]

        if quote:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == quote:
                quote = None
            continue

        if ch in ("'", '"', "`"):
            quote = ch
            continue

        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return i

    return -1

chosen = None
for match in starts:
    open_index = text.find("[", match.start())
    close_index = find_matching_bracket(text, open_index)
    if close_index < 0:
        continue

    context = text[max(0, match.start() - 900):min(len(text), close_index + 900)].lower()
    if "toda_espana" in context or "toda españa" in context or "toda espana" in context:
        chosen = (open_index, close_index)
        break

if chosen is None and len(starts) == 1:
    match = starts[0]
    open_index = text.find("[", match.start())
    close_index = find_matching_bracket(text, open_index)
    chosen = (open_index, close_index)

if chosen is None:
    print("ERROR: no puedo identificar municipiosPaths de Toda España")
    sys.exit(1)

open_index, close_index = chosen
body = text[open_index + 1:close_index]
all_scope_paths = set(re.findall(r"['\"]([^'\"]+_municipios\.geojson)['\"]", body))

missing_in_all_scope = [path for path in single_paths if path not in all_scope_paths]
missing_files = [path for path in single_paths if not Path("frontend/public" + path).exists()]

if missing_in_all_scope:
    print("ERROR: datasets individuales no incluidos en Toda España:")
    for path in missing_in_all_scope:
        print(" -", path)
    sys.exit(1)

if missing_files:
    print("ERROR: datasets declarados sin archivo publicado:")
    for path in missing_files:
        print(" -", path)
    sys.exit(1)

print(f"OK all-scope: {len(single_paths)} datasets individuales incluidos en Toda España")
