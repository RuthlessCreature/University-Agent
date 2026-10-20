"""下载固定版本官方WebR到本节私有构建目录，验证npm SRI并修正Windows导入路径。
不修改全局R、Node、Codex或任何密钥设置。不提供IBM SPSS运行环境。
"""
from pathlib import Path
import urllib.request,json,hashlib,base64,tarfile
R=Path(__file__).resolve().parent;dest=R.parent/'.build/webr-runtime';dest.mkdir(parents=True,exist_ok=True)
with urllib.request.urlopen('https://registry.npmjs.org/webr/0.6.0',timeout=30) as q:meta=json.load(q)
with urllib.request.urlopen(meta['dist']['tarball'],timeout=60) as q:data=q.read()
assert meta['dist']['integrity']=='sha512-'+base64.b64encode(hashlib.sha512(data).digest()).decode()
archive=dest/'webr-0.6.0.tgz';archive.write_bytes(data)
with tarfile.open(archive) as t:
 assert all((dest/m.name).resolve().is_relative_to(dest.resolve()) for m in t.getmembers())
 t.extractall(dest,filter='data')
p=dest/'package/dist/webr-worker.js';source=p.read_bytes();s=source.decode('utf-8')
old='let t=`${X.baseUrl}R.js`;Tt(t)'
new='let t=`${X.baseUrl}R.js`;if(/^[A-Za-z]:/.test(t))t="file:///"+t.replaceAll(String.fromCharCode(92),"/");Tt(t)'
assert old in s;s=s.replace(old,new,1)
old='await import((await import("path")).default.resolve(e))'
new='await import(e.startsWith("file:")?e:(await import("url")).pathToFileURL((await import("path")).default.resolve(e)).href)'
assert old in s;s=s.replace(old,new,1);p.write_text(s,'utf-8')
report={'package':'webr','version':'0.6.0','tarball':meta['dist']['tarball'],'npm_integrity':meta['dist']['integrity'],'integrity_verified':True,'original_worker_sha256':hashlib.sha256(source).hexdigest(),'patched_worker_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'R_wasm_sha256':hashlib.sha256((dest/'package/dist/R.wasm').read_bytes()).hexdigest(),'patch_scope':'Two Node.js Windows path-to-file-URL loader adjustments only; no R source or R.wasm changes.'}
(R/'r-runtime-provenance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
print('WebR 0.6.0 integrity verified; local runtime ready')
