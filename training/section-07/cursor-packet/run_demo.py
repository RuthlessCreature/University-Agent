"""Execute both supplied scripts locally; does not launch Cursor or call a model."""
from pathlib import Path
import datetime,hashlib,json,platform,subprocess,sys
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
events=[]
for name,folder in [('baseline.py','baseline-output'),('modified.py','modified-output')]:
    script=R/name;cmd=[sys.executable,str(script),str(R/'penguins.csv')]
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result=subprocess.run(cmd,cwd=R,capture_output=True,text=True,encoding='utf-8',errors='strict')
    event={'script':name,'cwd':str(R),'command':cmd,'started_at':started,
           'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr,
           'script_sha256':sha(script),'output_folder':folder}
    events.append(event)
    evidence={'executor':'local Python invoked by Codex; not Cursor','python_executable':sys.executable,
              'python_version':platform.python_version(),'cursor_operated':False,'cursor_model_called':False,
              'input_sha256':sha(R/'penguins.csv'),'runs':events,
              'scope':'Actual local script execution only; no scientific or teacher approval.'}
    (R/'run-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n','utf-8')
    if result.returncode:
        raise RuntimeError(f'{name} exited {result.returncode}: {result.stderr}')
subprocess.run([sys.executable,str(R/'check_results.py')],cwd=R,check=True)
