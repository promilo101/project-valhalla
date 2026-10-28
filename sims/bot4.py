import sys, json, time
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]; MINUTES = float(sys.argv[2]); WORKER = int(sys.argv[3]); WORKERS = int(sys.argv[4])
STRATS = ['none'] + ['el:' + m for m in ['jern', 'frost', 'ild', 'blod', 'lyn', 'rune']] + ['cls:' + c for c in ['warrior', 'archer', 'mage', 'priest']] + \
         ['relic:' + k for k in ['iron_oath', 'ember_boots', 'odins_eye', 'draugr_pact', 'huginn_feather', 'twin_souls', 'gleipnir_link', 'usurer_coin', 'mead_hall', 'berserk_mark', 'raven_banner', 'naglfar_chest']]
BOT = r"""
([seed, strat]) => {
  const V = window.VALHALLA;
  let rs = seed >>> 0; Math.random = () => { rs = (rs * 1664525 + 1013904223) >>> 0; return rs / 4294967296; };
  const [sk, sv] = strat.split(':');
  const fRelic = sk === 'relic' ? sv : null, fEl = sk === 'el' ? sv : fRelic === 'iron_oath' ? 'jern' : null, fCls = sk === 'cls' ? sv : null;
  const STAR = [1, 1.8, 3.2], tier = m => V.MODS[m].tier;
  const pw = u => STAR[u.star - 1] * (1 + .3 * (tier(u.mod) - 1));
  const focusB = u => (fEl && u.mod === fEl) || (fCls && u.cls === fCls) ? 1 : 0;
  const all = S => [...S.board, ...S.bench].filter(Boolean);
  const slotsOf = S => S.relics.includes('raven_banner') ? Math.min(9, S.level + 1) : Math.min(8, S.level);
  // value of a formation: unit strength times synergy steps it reaches, plus the chosen focus
  function boardValue(list){
    const c = {}, m = {}; for (const u of list){ c[u.cls] = (c[u.cls] || 0) + 1; m[u.mod] = (m[u.mod] || 0) + 1; }
    let v = 0; for (const u of list){ const cc = c[u.cls], mm = m[u.mod]; v += pw(u) * (1 + (cc >= 2 ? .2 : 0) + (cc >= 4 ? .3 : 0) + (mm >= 2 ? .15 : 0) + (mm >= 3 ? .15 : 0) + .6 * focusB(u)); }
    return v;
  }
  function arrange(S){
    const pool = all(S), slots = slotsOf(S), chosen = [];
    while (chosen.length < slots && pool.length){
      let best = -1, bv = -1; const base = boardValue(chosen);
      for (let i = 0; i < pool.length; i++){ const v = boardValue([...chosen, pool[i]]) - base; if (v > bv){ bv = v; best = i; } }
      chosen.push(pool.splice(best, 1)[0]);
    }
    S.board.fill(null); S.bench.fill(null);
    chosen.forEach((u, i) => { S.board[i] = u; });
    pool.sort((a, b) => pw(b) + focusB(b) - pw(a) - focusB(a)).slice(0, 8).forEach((u, i) => { S.bench[i] = u; });
  }
  // how much a shop card is wanted
  function cardWant(S, c){
    const own1 = all(S).filter(u => u.cls === c.cls && u.mod === c.mod && u.star === 1).length;
    const u = { cls: c.cls, mod: c.mod, star: 1 };
    let w = pw(u) + 1.6 * focusB(u) + (own1 >= 2 ? 3 : own1 === 1 ? 1.2 : 0);
    const onBoard = S.board.filter(Boolean), cc = onBoard.filter(x => x.cls === c.cls).length, mm = onBoard.filter(x => x.mod === c.mod).length;
    if (cc === 1 || cc === 3) w += .5; if (mm === 1 || mm === 2) w += .4;
    return w;
  }
  function weakest(S){ let wi = -1, wv = 1e9; S.bench.forEach((u, i) => { if (!u) return; const v = pw(u) + 1.6 * focusB(u) + (all(S).filter(x => x !== u && x.cls === u.cls && x.mod === u.mod && x.star === u.star).length) * 1.5; if (v < wv){ wv = v; wi = i; } }); return [wi, wv]; }
  const shopBot = (S) => {
    if (S.event && !S.event.done && S.event.type === 'shrine'){ const b = document.querySelector('#event [data-ev="' + (S.hero.hp > S.hero.maxHp * .6 ? 'accept' : 'leave') + '"]'); b && b.click(); }
    for (let pass = 0; pass < 8; pass++){
      if (S.level < 8 && S.gold >= 12 && (S.wave > 2 || S.gold >= 16)) V.buyXp();
      const offers = S.shop.map((c, i) => [c, i]).filter(x => x[0]).map(([c, i]) => [cardWant(S, c), c, i]).sort((a, b) => b[0] - a[0]);
      for (const [w, c, i] of offers){
        if (S.gold < tier(c.mod)) continue;
        const merge = all(S).filter(u => u.cls === c.cls && u.mod === c.mod && u.star === 1).length >= 2;
        if (S.bench.indexOf(null) < 0 && !merge){ const [wi, wv] = weakest(S); if (wi >= 0 && w > wv + .8){ V.sellAt('bench', wi); } else continue; }
        if (w < 1.15 && all(S).length >= slotsOf(S) + 3) continue;
        V.buy(i);
      }
      arrange(S);
      if (S.gold >= 8 + (S.wave >= 6 ? 10 : 0)) V.reroll(); else break;
    }
    if (S.hero.hp < S.hero.maxHp * .55 && S.gold >= 10){ const b = document.querySelector('#btnHeal'); b && b.click(); }
    arrange(S);
  };
  const dash = (h, S, nx, ny) => { if (h.dashCh <= 0 || h.dashT > 0) return false; h.dx = nx; h.dy = ny; h.dashT = .16; h.dashCh--; if (h.dashRt <= 0) h.dashRt = 2.5; S.bind = null; return true; };
  V.newRun();
  if (fRelic) V.gainRelic(fRelic);
  let frames = 0, result = null;
  while (frames < 60 * 60 * 60){
    const S = V.S;
    if (V.mode === 'over'){ result = 'died'; break; }
    if (S.wave >= 40){ result = 'capped'; break; }
    if (V.picking){ V.choosePick(Math.floor(Math.random() * 2)); if (V.picking) V.choosePick(0); continue; }
    if (V.mode === 'shop'){ S.event = S.event && S.event.type === 'shrine' ? S.event : null; shopBot(S); V.startWave(); continue; }
    if (V.mode === 'victory'){ V.enterEndless(); continue; }
    if (V.mode !== 'combat') break;
    const h = S.hero;
    if (S.endless && S.shopCd <= 0){ V.openEndlessShop(); continue; }
    let fx = 0, fy = 0;
    for (const e of S.enemies){ const dx = h.x - e.x, dy = h.y - e.y, d2 = dx*dx + dy*dy + 1; if (e.d.boss){ const d = Math.sqrt(d2); const pull = d > 100 ? -0.03 : d < 60 ? 0.05 : 0; fx += dx / d * pull; fy += dy / d * pull; } else if (d2 < 90*90){ fx += dx / d2; fy += dy / d2; }
      if ((e.mst === 'crouch' || e.mst === 'mark') && d2 < 130 * 130){ const side = Math.sign(-dx * e.ly + dy * e.lx) || 1; fx += -e.ly * side * .03; fy += e.lx * side * .03; } }
    for (const p of S.eprojs){ const dx = h.x - p.x, dy = h.y - p.y, d2 = dx*dx + dy*dy + 1; if (d2 < 40*40){ fx += dx / d2 * 2; fy += dy / d2 * 2; } }
    for (const tl of S.tele){ const dx = h.x - tl.x, dy = h.y - tl.y, d2 = dx*dx + dy*dy + 1; if (d2 < (tl.r + 26) ** 2){ fx += dx / d2 * 8; fy += dy / d2 * 8; } }
    fx += -h.y * 0.00002 - h.x * 0.00001; fy += h.x * 0.00002 - h.y * 0.00001;
    if (S.bind) dash(h, S, -h.dx, -h.dy);
    for (const c of S.chains) if (!c.snapped && c.t > c.wind - .12){ const ex = Math.cos(c.a), ey = Math.sin(c.a), rx = h.x - c.x, ry = h.y - c.y; if (Math.abs(rx * ey - ry * ex) < 10 && rx * ex + ry * ey > 0) dash(h, S, -ey, ex); }
    for (const L of S.lunges) if (L.state === 'wind' && L.t > L.wind - .1) dash(h, S, -L.uy, L.ux);
    if (frames % 30 === 0) for (let i = 0; i < 3; i++) if (S.abil[i] && S.abil[i].cd <= 0 && S.enemies.length) V.castAbility(i);
    const k = V.keys; k.KeyA = fx < -0.002; k.KeyD = fx > 0.002; k.KeyW = fy < -0.002; k.KeyS = fy > 0.002;
    V.update(1/60); frames++;
  }
  for (const kk in V.keys) V.keys[kk] = false;
  const S = V.S; if (!result) result = 'timeout';
  const rec = V.runRecord(result === 'died' ? 'died' : 'capped');
  if (S.won && result !== 'died') rec.result = 'won';
  rec.minutes = Math.round(frames / 3600 * 10) / 10;
  rec.data.strategy = strat;
  return rec;
}
"""
t0 = time.time(); n = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    while time.time() - t0 < MINUTES * 60:
        strat = STRATS[(n * WORKERS + WORKER) % len(STRATS)]
        pg = b.new_page(viewport={"width": 1280, "height": 720})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.route('**/*supabase.co/**', lambda r: r.fulfill(status=200, body='[]', headers={'content-type': 'application/json'}))
        pg.goto("file:///home/claude/valhalla/index.html"); pg.wait_for_timeout(400)
        pg.evaluate("()=>{try{localStorage.clear()}catch(e){}}")
        try:
            rec = pg.evaluate(BOT, [WORKER * 100000 + n * 7919 + 13, strat])
            rec['errors'] = errs[:3]
            with open(OUT, 'a') as f: f.write(json.dumps(rec) + "\n")
            print(n, strat, rec['result'], rec['wave'], round((time.time() - t0) / 60, 1), flush=True)
        except Exception as e:
            print('run failed', strat, str(e)[:200], flush=True)
        n += 1
        pg.close()
    b.close()
