"""Overnight bot run: start workers, stop when the raids add up to TARGET waves, then write the report.
usage: python3 run_night.py GAME_HTML OUT_DIR TARGET_WAVES [WORKERS] [MAX_MINUTES]"""
import sys, os, json, time, glob, subprocess
GAME, OUT, TARGET = sys.argv[1], sys.argv[2], int(sys.argv[3])
WORKERS = int(sys.argv[4]) if len(sys.argv) > 4 else 2
MAXMIN = float(sys.argv[5]) if len(sys.argv) > 5 else 330
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)
def waves():
    t = n = 0
    for f in glob.glob(os.path.join(OUT, 'w*.jsonl')):
        for l in open(f):
            l = l.strip()
            if l:
                try: t += json.loads(l)['wave']; n += 1
                except Exception: pass
    return t, n
procs = [subprocess.Popen(['python3', os.path.join(HERE, 'bot5_next.py'), os.path.join(OUT, f'w{i}.jsonl'), str(MAXMIN), str(i), str(WORKERS), GAME],
                          stdout=open(os.path.join(OUT, f'w{i}.log'), 'a'), stderr=subprocess.STDOUT) for i in range(WORKERS)]
t0 = time.time()
while True:
    time.sleep(30)
    w, n = waves()
    print(f'{(time.time() - t0) / 60:.0f} min: {n} raids, {w} waves', flush=True)
    if w >= TARGET or all(p.poll() is not None for p in procs) or time.time() - t0 > MAXMIN * 60 + 120: break
for p in procs:
    if p.poll() is None: p.terminate()
time.sleep(3)
subprocess.run(['python3', os.path.join(HERE, 'report_night.py'), OUT])
