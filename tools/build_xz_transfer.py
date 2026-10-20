#!/usr/bin/env python3
import base64, json, lzma, pathlib
root=pathlib.Path(__file__).resolve().parents[1]
src=sorted((root/"training/localization/en").glob("pages-???-???.json"))
slides=[z for p in src for z in json.loads(p.read_text(encoding="utf-8"))["items"]]
assert len(slides)==240 and [s["page"] for s in slides]==list(range(1,241))
payload=json.dumps({"schema":"university-en-v1","items":slides},ensure_ascii=False,separators=(",",":")).encode("utf-8")
packed=lzma.compress(payload,format=lzma.FORMAT_XZ,preset=9|lzma.PRESET_EXTREME)
text=base64.b64encode(packed).decode("ascii")
dest=root/"training/localization/en/bundle_xz";dest.mkdir(exist_ok=True)
for x in dest.glob("chunk-*.b64"):x.unlink()
C=12000
for i,start in enumerate(range(0,len(text),C),1):
  (dest/f"chunk-{i:03}.b64").write_text(text[start:start+C])
(dest/"stats.json").write_text(json.dumps({"slides":240,"source_chars":len(payload),"xz_bytes":len(packed),"base64_chars":len(text),"chunks":(len(text)+C-1)//C}))
print(len(packed),len(text),(len(text)+C-1)//C)
