import argparse,sys,pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'University-Skills'/'tools'))
from local_workflow import run,WorkflowError
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--template',required=True);p.add_argument('--output',required=True);p.add_argument('--guide');p.add_argument('--approval');p.add_argument('--final',action='store_true');a=p.parse_args()
try:print(json.dumps(run(a.input,a.template,a.output,a.approval,a.final,a.guide),ensure_ascii=False,indent=2))
except (WorkflowError,ValueError) as e:print(json.dumps({'error':str(e)},ensure_ascii=False));sys.exit(2)
