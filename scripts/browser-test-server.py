"""Disposable local API/target for browser tests; no live modules or secrets."""
import os
import subprocess
import sys
import time
env=os.environ.copy()
env.update(DATA_MODE='demo',OPERATOR_TOKEN='browser-test-disposable-token-0000000000',FAKE_RUNTIME_ENABLED='false')
processes=[]
try:
    for app,port in [('app.demo_target:app','8090'),('app.main:create_app','8000')]:
        command=[sys.executable,'-m','uvicorn',app,'--host','127.0.0.1','--port',port,'--no-access-log','--log-level','critical']
        if app.endswith('create_app'): command.append('--factory')
        processes.append(subprocess.Popen(command,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL))
    while all(p.poll() is None for p in processes): time.sleep(.2)
    raise SystemExit(1)
finally:
    for p in processes:
        p.terminate()
    for p in processes:
        try: p.wait(timeout=3)
        except subprocess.TimeoutExpired: p.kill()
