"""Summarise bot raids in OUT_DIR/w*.jsonl into OUT_DIR/report.md"""
import sys, os, json, glob, collections, statistics as st
OUT = sys.argv[1]
R = []
for f in sorted(glob.glob(os.path.join(OUT, 'w*.jsonl'))):
    for l in open(f):
        l = l.strip()
        if l:
            try: R.append(json.loads(l))
            except Exception: pass
L = []
P = L.append
if not R:
    open(os.path.join(OUT, 'report.md'), 'w').write('# Bot report\n\nNo raids finished.\n'); sys.exit()
W = [r['wave'] for r in R]
pct = lambda a, b: f'{100 * a / b:.0f}%' if b else '–'
ver = R[0].get('version', '?')
P(f'# Overnight bot report, version {ver}\n')
P(f'{len(R)} raids, {sum(W)} waves in total. Average best wave {st.mean(W):.1f}, median {st.median(W)}. '
  f'Reached wave 10: {pct(sum(w >= 10 for w in W), len(W))}, wave 20 (Fenrir beaten): {pct(sum(w > 20 for w in W), len(W))}, wave 30: {pct(sum(w >= 30 for w in W), len(W))}, capped at 40: {pct(sum(w >= 40 for w in W), len(W))}.\n')
P('The bot buys units for synergies, buys gear upgrades from the Merchant, takes boss gear when it is an upgrade, and uses battlefield events. "gear:none" never buys gear, "gear:focus" spends more on it, "events:none" ignores battlefield events.\n')
# strategies
by = collections.defaultdict(list)
for r in R: by[r['data'].get('strategy', '?')].append(r)
P('## Strategies\n\n| Strategy | Raids | Avg wave | Median | Beat Fenrir | Top killer |\n| --- | --- | --- | --- | --- | --- |')
for k, rs in sorted(by.items(), key=lambda kv: -st.mean([r['wave'] for r in kv[1]])):
    ws = [r['wave'] for r in rs]; kl = collections.Counter(r['data'].get('killer') for r in rs if r['result'] == 'died').most_common(1)
    P(f'| {k} | {len(rs)} | {st.mean(ws):.1f} | {st.median(ws)} | {pct(sum(w > 20 for w in ws), len(ws))} | {kl[0][0] if kl else "–"} |')
# killers and damage
died = [r for r in R if r['result'] == 'died']
P('\n## What ends raids\n\n| Killer | Deaths | Share |\n| --- | --- | --- |')
for k, n in collections.Counter(r['data'].get('killer') for r in died).most_common(12): P(f'| {k} | {n} | {pct(n, len(died))} |')
T = collections.Counter()
for r in R:
    for k, v in (r['data'].get('taken') or {}).items(): T[k.split(':')[0].replace('Elite ', '')] += v
tot = sum(T.values()) or 1
P('\n## Damage taken by source\n\n| Source | Share |\n| --- | --- |')
for k, v in T.most_common(12): P(f'| {k} | {100 * v / tot:.1f}% |')
# gear
P('\n## Gear\n')
gb = [len(r['data'].get('gearBuys') or []) for r in R]
boss = [sum(1 for g in (r['data'].get('gearBuys') or []) if g.get('boss')) for r in R]
P(f'Pieces taken per raid: {st.mean(gb):.1f} on average, of which {st.mean(boss):.1f} from bosses.\n')
rar = collections.Counter(g.get('r') for r in R for g in (r['data'].get('gearBuys') or []))
P('| Rarity | Pieces |\n| --- | --- |'); [P(f'| {["Common", "Rare", "Epic"][k] if k in (0, 1, 2) else k} | {n} |') for k, n in sorted(rar.items(), key=lambda x: str(x[0]))]
# events
P('\n## Battlefield events\n\n| Event | Appeared | Used | Used share |\n| --- | --- | --- | --- |')
EV = collections.Counter(); EA = collections.Counter()
for r in R:
    for e in r['data'].get('events') or []:
        if e['t'] == 'merchant': continue
        EV[e['t']] += 1; EA[e['t']] += 1 if e.get('a') else 0
for k in EV: P(f'| {k} | {EV[k]} | {EA[k]} | {pct(EA[k], EV[k])} |')
# gold
gpw = [sum((r['data'].get('earned') or {}).values()) / max(1, r['wave']) for r in R if isinstance(r['data'].get('earned'), dict)]
spw = [(r['data'].get('earned') or {}).get('Souls', 0) / max(1, r['wave']) for r in R if isinstance(r['data'].get('earned'), dict)]
if gpw: P(f'\n## Economy\n\nGold per wave {st.mean(gpw):.1f}, of which from souls {st.mean(spw):.1f}.\n')
errs = [e for r in R for e in (r.get('errors') or [])]
if errs: P('\n## Errors seen\n\n' + '\n'.join(f'- {e[:200]}' for e in sorted(set(errs))[:10]))
open(os.path.join(OUT, 'report.md'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
