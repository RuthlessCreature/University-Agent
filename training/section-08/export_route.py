"""Compatibility entry point for the shared editable-diagram exporter."""
from pathlib import Path
import os,subprocess
r=Path(__file__).resolve().parent
node=os.environ.get('RUNTIME_NODE','C:/Users/Georgij Xe/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe')
subprocess.run([node,str(r/'export_diagrams.mjs')],check=True)
