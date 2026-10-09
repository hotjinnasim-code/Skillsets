from pathlib import Path
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone

work = Path.cwd().resolve()
out = work / "coordinator/guides/m3-m4"
source = out / "m3-layout.json"
spec = json.loads(source.read_text())
before_text = json.dumps(spec["text_blocks"], ensure_ascii=False, sort_keys=True)
old_arms = [spec["shapes"][3], spec["shapes"][4]]
spec["shapes"][3]["points"] = [[268, 420], [350, 442], [390, 704], [555, 752], [841, 779], [850, 831], [522, 814], [430, 750], [318, 749], [280, 620]]
spec["shapes"][4]["points"] = [[328, 508], [385, 575], [429, 736], [836, 834], [1106, 809], [1149, 756], [1193, 766], [1140, 854], [830, 884], [490, 800], [430, 752], [325, 670]]
assert json.dumps(spec["text_blocks"], ensure_ascii=False, sort_keys=True) == before_text
target = out / "m3-layout-v2.json"
with target.open("x") as f:
    json.dump(spec, f, ensure_ascii=False, indent=2)
    f.write("\n")
renderer = work / "snapshots/candidate-w/scripts/make_layout_guide.py"
argv = [sys.executable, "-B", str(renderer), str(target), "--output-dir", str(out), "--name", "m3-guide-v2"]
completed = subprocess.run(argv, cwd=work, capture_output=True, text=True)
def pin(p):
    b = p.read_bytes()
    return {"path": str(p), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
record = {"recorded_utc": datetime.now(timezone.utc).isoformat(), "role": "R20-C1-M3",
          "reason": "Original-detail view found the authored sleeve/forearm boundary touching the final lower-left identity glyph. Narrowed only those planning contours left of x430; text copy/fonts/positions/lines and original plan remain unchanged.",
          "source": pin(source), "spec": pin(target), "argv": argv, "cwd": str(work),
          "exit_code": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr,
          "changed_shape_indices": [3, 4], "before_shapes": old_arms,
          "after_shapes": [spec["shapes"][3], spec["shapes"][4]],
          "text_unchanged": True, "native_calls": 0, "final_poster_edits": 0}
if completed.returncode == 0:
    record["outputs"] = [pin(out / ("m3-guide-v2" + s)) for s in [".svg", ".png", ".manifest.json"]]
with (out / "m3-technical-adjustment.json").open("x") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(json.dumps({"exit_code": completed.returncode, "stderr": completed.stderr, "record": str(out / "m3-technical-adjustment.json")}))
