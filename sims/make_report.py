import json, glob, os, statistics as st
D = '/tmp/claude-0/-home-claude/a322939f-fb67-5ade-89b1-ffec1ea148e7/scratchpad/'
rows = []
for f in sorted(glob.glob(D + 'sim2_*.jsonl')):
    for line in open(f):
        line = line.strip()
        if not line: continue
        r = json.loads(line); r['created_at'] = '2026-10-28T21:45:00Z'; r['build'] = 'bot'; r['debug'] = False
        rows.append(r)
print('runs', len(rows))
src = open('/home/claude/valhalla/stats.html').read()
# embed the data instead of reading Supabase
start = src.index('async function load(){'); end = src.index("for (const id of ['#fVer'")
load = """async function load(){
  all = window.BOT_RUNS;
  const uniq = f => [...new Set(all.map(f).filter(Boolean))];
  fillSelect($('#fVer'), uniq(r => r.version)); fillSelect($('#fHero'), uniq(r => r.hero)); fillSelect($('#fMap'), uniq(r => r.map));
  $('#status').textContent = `${all.length} bot raids`;
  render();
}
"""
src = src[:start] + load + src[end:]
src = src.replace("<option value=\"public\">Public</option><option value=\"dev\">Dev</option><option value=\"\">Both</option>", "<option value=\"\">Bot runs</option>")
src = src.replace("(b === '' || (b === 'dev' ? r.build === 'dev' : r.build !== 'dev'))", "true")
src = src.replace("<title>Valhalla Balance Stats</title>", "<title>Valhalla Bot Balance Report</title>")
src = src.replace("Project Valhalla <span>balance stats</span>", "Bot balance <span>report</span>")
src = src.replace("Anonymous run records from players who chose to share them. Rows with fewer than 5 runs are greyed out, because small samples are mostly noise.",
  f"{len(rows)} raids played by the autoplay bot on version 0.16.0, stopped at Endless wave 40. Each raid forces one focus (an element, a class or a relic), and the bot shops, sells and arranges its formation for strength and synergies around it. It takes a random ability offer, dodges telegraphs and never buys other relics. This shows how the game's numbers compare, not how real players play. Compare against \"No focus\" in the strategy table. Rows with fewer than 5 runs are greyed out.")
src = src.replace('<button type="button" id="btnReload">Reload</button>', '')
src = src.replace('<div class="grid">', '<section class="card"><h2>Strategies, head to head</h2><p class="note" style="margin-bottom:6px">Each raid was played with one forced focus: an element, a class or a relic. "None" means no focus and no relics. Same bot, same number of raids each.</p><div class="scroll"><table class="tbl" id="tStrat"></table></div></section>\n  <div class="grid">', 1)
src = src.replace("  // killers", '''  const SN = k => { if (k === 'none') return 'No focus'; const [a, b] = k.split(':'); return a === 'el' ? 'Element: ' + (EL[b] || b) : a === 'cls' ? 'Class: ' + (CL[b] || b) + 's' : 'Relic: ' + (RL[b] || b); };
  const sm = new Map(); for (const r of runs){ const k = (r.data && r.data.strategy) || 'none'; if (!sm.has(k)) sm.set(k, []); sm.get(k).push(r); }
  const sl = [...sm.entries()].map(([k, rs]) => ({ k, n: rs.length, wave: avg(rs.map(r => r.wave)), beat: rs.filter(beat).length / rs.length, med: median(rs.map(r => r.wave)) })).sort((a, b) => b.wave - a.wave);
  const swm = Math.max(1, ...sl.map(x => x.wave)), sbase = (sm.get('none') || []).length ? avg(sm.get('none').map(r => r.wave)) : avg(runs.map(r => r.wave));
  table($('#tStrat'), ['Strategy', 'Raids', 'Average wave', 'Median', 'Beat Fenrir', ''], sl.map(x => `<tr class="${x.n < 5 ? 'few' : ''}"><td>${esc(SN(x.k))}</td><td>${x.n}</td><td>${x.wave.toFixed(1)} <small style="color:${x.wave >= sbase ? 'var(--good)' : 'var(--bad)'}">${x.wave >= sbase ? '+' : ''}${(x.wave - sbase).toFixed(1)}</small></td><td>${x.med}</td><td>${pct(x.beat)}</td><td class="bar">${bar(x.wave, swm, x.k.startsWith('relic') ? 'var(--frost)' : x.k.startsWith('cls') ? 'var(--ember)' : 'var(--gold)')}</td></tr>`));
  // killers''', 1)
src = src.replace('<script>', '<script>window.BOT_RUNS = ' + json.dumps(rows) + ';\n', 1)
# artifact page contract: drop doctype/html/head/body wrappers, keep title and styles at the top
src = src.replace('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n', '')
src = src.replace('</head>\n<body>\n', '').replace('</body>\n</html>\n', '')
os.makedirs('/home/claude/bot-report', exist_ok=True)
open('/home/claude/bot-report/bot-report.html', 'w').write(src)
json.dump(rows, open(D + 'sim_all.json', 'w'))
