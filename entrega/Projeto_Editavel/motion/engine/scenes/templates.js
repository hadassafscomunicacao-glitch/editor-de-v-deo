// ---------- Reusable typographic / diagram templates. All times are seconds relative to scene start.
// Common: P.dur, P.out (exit start, default dur-0.5)
const SAFE_X = 76, TOP_ZONE = 170;

// word spans helper: tokens [{text, cls, t}] -> spans
function buildWords(parent, line, baseStyle) {
  const L = el('div', { style: Object.assign({ display: 'block', whiteSpace: 'normal', textWrap: 'balance' }, baseStyle || {}) }, parent);
  return line.map(w => {
    const s = el('span', { class: 'w ' + (w.cls || ''), style: { display: 'inline-block', marginRight: w.noSpace ? '0' : '0.24em', willChange: 'transform' } }, L, w.text);
    return { s, w };
  });
}
const STY = {
  sans: { font: "700 74px 'Inter Tight'", color: '#fff', letterSpacing: '-0.015em' },
  sansM: { font: "600 54px 'Inter Tight'", color: '#fff', letterSpacing: '-0.01em' },
  serif: { font: "italic 400 82px 'Fraunces'", color: PAL.goldL, letterSpacing: '-0.01em' },
  serifW: { font: "italic 400 82px 'Fraunces'", color: '#fff' },
};
function styleFor(cls, size) {
  const map = { gold: { color: PAL.goldL }, serif: { fontFamily: 'Fraunces', fontStyle: 'italic', fontWeight: 400 }, light: { fontWeight: 500, opacity: .9 }, red: { color: '#F0A893' } };
  const o = {}; (cls || '').split(' ').forEach(c => Object.assign(o, map[c] || {})); return o;
}

// LETTERING: P.lines = [{words:[{text,cls,t}], size, weight, font:'sans'|'serif', gap}], P.top, P.align, P.kicker, P.kickerT, P.mode ('words'|'line'), P.underline {line, word}
SCENES.lettering = (root, P) => {
  const box = el('div', { class: 'abs shadow', style: { left: SAFE_X + 'px', width: (1080 - 2 * SAFE_X) + 'px', top: (P.top ?? TOP_ZONE) + 'px', textAlign: P.align || 'center' } }, root);
  let kick = null;
  if (P.kicker) kick = el('div', { class: 'kicker', style: { marginBottom: '22px', fontSize: (P.kickerSize || 24) + 'px', textShadow: 'none' } }, box, P.kicker);
  const all = [];
  P.lines.forEach((ln, li) => {
    const base = ln.font === 'serif' ? { font: `italic ${ln.weight || 400} ${ln.size || 80}px 'Fraunces'`, color: ln.color || PAL.goldL, lineHeight: 1.08 }
      : { font: `${ln.weight || 700} ${ln.size || 72}px 'Inter Tight'`, color: ln.color || '#fff', letterSpacing: '-0.018em', lineHeight: 1.08 };
    base.marginTop = (ln.gap ?? (li ? 6 : 0)) + 'px';
    const ws = buildWords(box, ln.words, base);
    ws.forEach(x => Object.assign(x.s.style, styleFor(x.w.cls)));
    all.push(...ws);
  });
  const out = P.out ?? (P.dur - .55);
  return t => {
    const ex = 1 - E.inOutCubic(clamp((t - out) / .5));
    if (kick) rise(kick, prog(t, P.kickerT ?? 0, .55) * ex, 14, 4);
    all.forEach(({ s, w }) => {
      const k = prog(t, w.t ?? 0, w.d ?? .5, E.outCubic);
      const a = k * ex;
      s.style.opacity = a;
      const sc = w.pop ? (0.86 + 0.14 * E.outBack(clamp((t - (w.t ?? 0)) / .55), 1.4)) : 1;
      s.style.transform = `translateY(${(1 - k) * (w.dy ?? 26) + (1 - ex) * -10}px) scale(${sc})`;
      s.style.filter = k < 1 ? `blur(${(1 - k) * 7}px)` : 'none';
    });
  };
};

// NAME TAG near a participant: P.side 'L'|'R', P.name, P.role, P.y
SCENES.nameTag = (root, P) => {
  const cx = P.side === 'L' ? (P.x ?? 250) : (P.x ?? 815);
  const g = el('div', { class: 'abs', style: { left: (cx - 300) + 'px', width: '600px', top: (P.y ?? 545) + 'px', textAlign: 'center' } }, root);
  const nm = el('div', { class: 'serif shadow', style: { fontSize: '50px', fontWeight: 400, color: '#fff', lineHeight: 1 } }, g, P.name);
  const ln = el('div', { style: { margin: '14px auto 12px', height: '2px', width: '0px', background: PAL.gold } }, g);
  const rl = el('div', { class: 'sans', style: { font: "600 22px 'Inter Tight'", letterSpacing: '.24em', textTransform: 'uppercase', color: PAL.goldL, textShadow: '0 2px 12px rgba(0,0,0,.6)' } }, g, P.role);
  const out = P.out ?? (P.dur - .5);
  return t => {
    const ex = 1 - E.inOutCubic(clamp((t - out) / .45));
    rise(nm, prog(t, 0, .6) * ex, 18, 6);
    ln.style.width = (140 * prog(t, .2, .7, E.outQuart)) + 'px'; ln.style.opacity = ex;
    rise(rl, prog(t, .35, .6) * ex, 12, 4);
  };
};

// LIST: P.kicker, P.items [{n, text, sub, t}], P.top, P.style 'numbers'|'checks'
SCENES.list = (root, P) => {
  const box = el('div', { class: 'abs', style: { left: (P.left ?? 110) + 'px', width: (P.width ?? 860) + 'px', top: (P.top ?? 150) + 'px' } }, root);
  const kick = P.kicker ? el('div', { class: 'kicker', style: { marginBottom: '26px', fontSize: '23px' } }, box, P.kicker) : null;
  const rows = P.items.map((it, i) => {
    const r = el('div', { style: { display: 'flex', alignItems: 'baseline', gap: '26px', marginBottom: (P.rowGap ?? 20) + 'px' } }, box);
    const n = el('div', { class: 'serif', style: { fontSize: (P.numSize ?? 44) + 'px', fontStyle: 'italic', color: it.numColor || PAL.goldL, minWidth: (P.numW ?? 70) + 'px', textShadow: '0 4px 20px rgba(0,0,0,.5)' } }, r, it.n ?? String(i + 1).padStart(2, '0'));
    const tx = el('div', { class: 'shadow', style: { font: `${it.weight || 650} ${it.size || P.size || 48}px 'Inter Tight'`, color: it.color || '#fff', letterSpacing: '-0.01em', lineHeight: 1.12 } }, r, it.text + (it.sub ? `<div style="font:500 ${P.subSize || 27}px 'Inter Tight';color:rgba(245,240,230,.78);margin-top:6px;letter-spacing:0">${it.sub}</div>` : ''));
    let strike = null;
    if (it.strikeT != null) strike = el('div', { class: 'abs', style: { height: '4px', background: '#E07A62', left: 0, top: '50%', width: '0%', borderRadius: '2px' } }, tx), tx.style.position = 'relative';
    return { r, it, strike, tx };
  });
  const out = P.out ?? (P.dur - .55);
  return t => {
    const ex = 1 - E.inOutCubic(clamp((t - out) / .5));
    if (kick) rise(kick, prog(t, P.kickerT ?? 0, .5) * ex, 12, 4);
    rows.forEach(({ r, it, strike, tx }) => {
      const k = prog(t, it.t, .55);
      r.style.opacity = k * ex * (it.dimAt != null && t > it.dimAt ? .38 : 1);
      r.style.transform = `translateX(${(1 - k) * -30}px)`; r.style.filter = k < 1 ? `blur(${(1 - k) * 6}px)` : 'none';
      if (strike) strike.style.width = (100 * prog(t, it.strikeT, .45, E.inOutCubic)) + '%';
      if (it.hiT != null) { const h = prog(t, it.hiT, .5); tx.style.color = h > .5 ? PAL.goldL : (it.color || '#fff'); r.style.transform += ` scale(${1 + .06 * h})`; r.style.transformOrigin = 'left center'; }
    });
  };
};

// CONTRAST (two columns): P.left {title, sub, items:[{text, mark:'ok'|'no', t}], t}, P.right {...}, P.top, P.vs
SCENES.contrast = (root, P) => {
  const top = P.top ?? 150;
  const mk = (side, cfg) => {
    const x = side === 'L' ? 70 : 560;
    const c = el('div', { class: 'abs', style: { left: x + 'px', width: '450px', top: top + 'px', textAlign: 'left' } }, root);
    const k = cfg.kicker ? el('div', { class: 'kicker', style: { fontSize: '20px', marginBottom: '12px', color: cfg.kColor || PAL.goldL } }, c, cfg.kicker) : null;
    const ti = el('div', { class: 'serif shadow', style: { fontSize: (cfg.size || 58) + 'px', color: '#fff', lineHeight: 1.04 } }, c, cfg.title);
    const bar = el('div', { style: { height: '3px', width: '0px', background: cfg.color || PAL.gold, margin: '16px 0 18px' } }, c);
    const items = (cfg.items || []).map(it => {
      const r = el('div', { class: 'shadow', style: { font: "600 31px 'Inter Tight'", color: 'rgba(255,255,255,.95)', marginBottom: '12px', display: 'flex', gap: '14px', alignItems: 'baseline', lineHeight: 1.18 } }, c);
      el('span', { style: { color: it.mark === 'no' ? '#F0A893' : (it.mark === 'ok' ? '#9FD3C7' : PAL.goldL), fontWeight: 800, minWidth: '30px' } }, r, it.mark === 'no' ? '✕' : (it.mark === 'ok' ? '✓' : '•'));
      el('span', {}, r, it.text);
      return { r, it };
    });
    return { c, k, ti, bar, items, cfg };
  };
  const cols = [mk('L', P.left), mk('R', P.right)];
  const div = el('div', { class: 'abs', style: { left: '539px', top: (top - 6) + 'px', width: '2px', height: '0px', background: 'linear-gradient(rgba(201,165,95,0), rgba(201,165,95,.9), rgba(201,165,95,0))' } }, root);
  const vs = P.vs ? el('div', { class: 'abs serif', style: { left: '500px', width: '80px', textAlign: 'center', top: (top + 60) + 'px', fontSize: '40px', fontStyle: 'italic', color: PAL.goldL, opacity: 0 } }, root, P.vs) : null;
  const out = P.out ?? (P.dur - .55);
  return t => {
    const ex = 1 - E.inOutCubic(clamp((t - out) / .5));
    const t0 = Math.min(P.left.t, P.right.t);
    div.style.height = (P.divH ?? 330) * prog(t, t0, .9, E.inOutCubic) + 'px'; div.style.opacity = ex;
    if (vs) vs.style.opacity = prog(t, t0 + .3, .5) * ex;
    cols.forEach(({ k, ti, bar, items, cfg }, ci) => {
      const kk = prog(t, cfg.t, .6) * ex;
      if (k) rise(k, kk, 12, 4);
      rise(ti, kk, 22, 6);
      bar.style.width = (90 * prog(t, cfg.t + .15, .7, E.outQuart)) + 'px'; bar.style.opacity = ex;
      items.forEach(({ r, it }) => { const a = prog(t, it.t, .5); rise(r, a * ex * (it.dimAt != null && t > it.dimAt ? .4 : 1), 14, 5); });
      if (cfg.dimAt != null && t > cfg.dimAt) { ti.style.opacity = Math.min(+ti.style.opacity, .45); }
    });
  };
};

// CHAIN: P.nodes [{text, t}], vertical or horizontal flow with arrows; P.top, P.dir 'v'|'h'
SCENES.chain = (root, P) => {
  const box = el('div', { class: 'abs', style: { left: '90px', width: '900px', top: (P.top ?? 150) + 'px', display: 'flex', flexDirection: 'column', alignItems: 'center' } }, root);
  const kick = P.kicker ? el('div', { class: 'kicker', style: { marginBottom: '22px', fontSize: '22px' } }, box, P.kicker) : null;
  const parts = [];
  P.nodes.forEach((n, i) => {
    if (i) { const a = el('div', { style: { width: '2px', height: (P.arrowH ?? 34) + 'px', background: PAL.gold, position: 'relative', margin: '6px 0' } }, box); el('div', { style: { position: 'absolute', left: '-7px', bottom: '-4px', width: 0, height: 0, borderLeft: '8px solid transparent', borderRight: '8px solid transparent', borderTop: `11px solid ${PAL.gold}` } }, a); parts.push({ type: 'a', e: a, t: n.t - .25 }); }
    const nd = el('div', { class: 'shadow', style: { font: `${n.weight || 650} ${n.size || P.size || 44}px 'Inter Tight'`, color: n.color || '#fff', padding: '10px 26px', borderRadius: '14px', border: n.box ? '1.5px solid rgba(201,165,95,.7)' : 'none', background: n.box ? 'rgba(20,35,54,.55)' : 'transparent', textAlign: 'center', lineHeight: 1.12 } }, box, n.text);
    if (n.cls) Object.assign(nd.style, styleFor(n.cls));
    parts.push({ type: 'n', e: nd, t: n.t });
  });
  const out = P.out ?? (P.dur - .55);
  return t => {
    const ex = 1 - E.inOutCubic(clamp((t - out) / .5));
    if (kick) rise(kick, prog(t, P.kickerT ?? 0, .5) * ex, 12, 4);
    parts.forEach(p => {
      const k = prog(t, p.t, p.type === 'a' ? .4 : .55);
      if (p.type === 'a') { p.e.style.opacity = ex * (k > 0 ? 1 : 0); p.e.style.transform = `scaleY(${k})`; p.e.style.transformOrigin = 'top'; }
      else rise(p.e, k * ex, 18, 6);
    });
  };
};

// SECTION CARD for the four steps: P.n (1..4), P.title, P.kicker
SCENES.stepCard = (root, P) => {
  const names = P.names || ['Diagnóstico', 'Estrutura', 'Implementação', 'Liderança'];
  const box = el('div', { class: 'abs', style: { left: 0, width: '1080px', top: (P.top ?? 165) + 'px', textAlign: 'center' } }, root);
  const kick = el('div', { class: 'kicker', style: { fontSize: '24px', marginBottom: '16px' } }, box, P.kicker || `Etapa ${P.n}`);
  const ti = el('div', { class: 'serif shadow', style: { fontSize: '104px', color: '#fff', lineHeight: 1 } }, box, P.title || names[P.n - 1]);
  const dots = el('div', { style: { display: 'flex', justifyContent: 'center', gap: '18px', marginTop: '30px' } }, box);
  const ds = names.map((nm, i) => {
    const d = el('div', { style: { display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px', width: '190px' } }, dots);
    const bar = el('div', { style: { height: '4px', width: '100%', borderRadius: '2px', background: i < P.n - 1 ? 'rgba(201,165,95,.55)' : (i === P.n - 1 ? PAL.goldL : 'rgba(255,255,255,.22)') } }, d);
    const lb = el('div', { style: { font: "600 18px 'Inter Tight'", letterSpacing: '.14em', textTransform: 'uppercase', color: i === P.n - 1 ? PAL.goldL : 'rgba(255,255,255,.55)', textShadow: '0 2px 10px rgba(0,0,0,.6)' } }, d, nm);
    return { d, bar, lb, i };
  });
  const out = P.out ?? (P.dur - .55);
  return t => {
    const ex = 1 - E.inOutCubic(clamp((t - out) / .5));
    rise(kick, prog(t, 0, .5) * ex, 12, 4); rise(ti, prog(t, .12, .7) * ex, 26, 8);
    ds.forEach(({ d, bar, i }) => { const k = prog(t, .45 + i * .09, .5); d.style.opacity = k * ex; d.style.transform = `translateY(${(1 - k) * 10}px)`; });
  };
};

// QUOTE: P.text (html allowed), P.attrib, P.top
SCENES.quote = (root, P) => {
  const box = el('div', { class: 'abs', style: { left: '100px', width: '880px', top: (P.top ?? 170) + 'px', textAlign: 'center' } }, root);
  const qm = el('div', { class: 'serif', style: { fontSize: '150px', lineHeight: .6, color: PAL.gold, height: '70px' } }, box, '“');
  const tx = el('div', { class: 'serif shadow', style: { fontSize: (P.size || 62) + 'px', fontStyle: 'italic', color: '#fff', lineHeight: 1.16 } }, box, P.text);
  const at = P.attrib ? el('div', { class: 'kicker', style: { marginTop: '22px', fontSize: '20px' } }, box, P.attrib) : null;
  const out = P.out ?? (P.dur - .55);
  return t => {
    const ex = 1 - E.inOutCubic(clamp((t - out) / .5));
    rise(qm, prog(t, 0, .6) * ex, 10, 4); rise(tx, prog(t, .15, .8) * ex, 20, 8); if (at) rise(at, prog(t, .6, .6) * ex, 10, 4);
  };
};
