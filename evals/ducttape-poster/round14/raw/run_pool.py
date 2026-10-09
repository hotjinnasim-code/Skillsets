"""Run a frozen job queue once, bounding fresh CLI worker processes."""
import argparse,concurrent.futures,datetime,json,subprocess,sys,threading
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--queue',type=Path,required=True);p.add_argument('--journal',type=Path,required=True);p.add_argument('--workers',type=int,default=3);a=p.parse_args()
if not 1<=a.workers<=3:raise ValueError('Root plus at most three fresh workers')
jobs=json.loads(a.queue.read_text());assert isinstance(jobs,list) and len(jobs)==len(set(jobs))
lock=threading.Lock();active=0;peak=0
runner=Path(__file__).with_name('run_agent.py')
with a.journal.open('x') as journal:
 def event(kind,**kwargs):
  row={'event':kind,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),**kwargs};journal.write(json.dumps(row)+'\n');journal.flush();print(json.dumps(row),flush=True)
 def run(job):
  global active,peak
  with lock:
   active+=1;peak=max(peak,active);event('launch',job=job,active_workers=active)
  result=subprocess.run([sys.executable,str(runner),'--job',job],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
  with lock:
   active-=1;event('close',job=job,runner_exit=result.returncode,runner_output=result.stdout,active_workers=active)
  return result.returncode
 event('queue_frozen',queue=str(a.queue.resolve()),jobs=len(jobs),configured_worker_max=a.workers,native_concurrency_semantics='worker process bounds; inspect actual caller intervals separately')
 with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:codes=list(pool.map(run,jobs))
 event('pool_closed',peak_worker_processes=peak,jobs=len(jobs),nonzero_runner_exits=sum(c!=0 for c in codes))
