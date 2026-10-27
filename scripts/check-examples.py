"""Execute every downloadable tutorial with a noninteractive plotting backend."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='hub-python-') as temp:
    env={**os.environ,'MPLBACKEND':'Agg','MPLCONFIGDIR':temp}
    failures=[]
    for script in sorted((root/'examples').glob('*.py')):
        result=subprocess.run([sys.executable,str(script)],capture_output=True,text=True,timeout=120,env=env)
        print(f'{"PASS" if result.returncode == 0 else "FAIL"} {script.name}',flush=True)
        if result.returncode:
            failures.append(script.name)
            print(result.stdout+result.stderr)
    if failures: sys.exit(1)
