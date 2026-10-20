#!/usr/bin/env python3
"""Bundle reviewed translation segments for deterministic PPTX localization.
Only the english text map and notes are bundled; the original pptx is not changed.
"""
import base64, glob, json, pathlib, zlib
root=pathlib.Path(__file__).resolve().parents[1]
files=sorted((root/"training/localization/en").glob("pages-???-???.json"))
items=[]
for f in files:
    data=json.loads(f.read_text(encoding="utf-8"))
    items += data["items"]
nums=[x["page"] for x in items]
if sorted(nums)!=list(range(1,241)):
    raise SystemExit(f"Expected 240 pages, got {len(nums)} or duplicate/missing page IDs")
for x in items:
    if not x.get("note") or any(not q[1] for q in x["pairs"]):
        raise SystemExit("Missing translated text on slide "+str(x["page"]))
text=json.dumps({"schema":"university-english-localization-v1","items":items},ensure_ascii=False,separators=(",",":"))
compressed=zlib.compress(text.encode("utf-8"),9)
encoded=base64.b64encode(compressed).decode("ascii")
directory=root/"training/localization/en/bundle"
directory.mkdir(parents=True,exist_ok=True)
for old in directory.glob("chunk-*.b64"):
    old.unlink()
CHUNK=16000
for i,start in enumerate(range(0,len(encoded),CHUNK),1):
    (directory/f"chunk-{i:03d}.b64").write_text(encoded[start:start+CHUNK],encoding="ascii")
(directory/"bundle-stats.json").write_text(json.dumps({"pages":len(items),"lines":sum(len(x["pairs"]) for x in items),"uncompressed_chars":len(text),"compressed_bytes":len(compressed),"base64_chars":len(encoded),"chunks":(len(encoded)+CHUNK-1)//CHUNK},indent=2),encoding="utf-8")
print("Bundled",len(items),"slides,",len(encoded),"base64 characters")
