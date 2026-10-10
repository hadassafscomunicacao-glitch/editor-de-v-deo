// "O elevador do conflito" — building cross-section, cabin moving between floors as the presenters speak.
// params: dur, header, sub, floors:[{level,name,desc,t(row reveal + default stop)}], stops:[{t,floor}] (default: floors' t),
//         startFloor, rowsDim, pills:[{t,text}], freio:t, accel:{t,text,t2,text2}, topNote:{t,text}, closing, closingAt, panelH
SCENES.elevator = (root, P) => {
  const W = 1080, PH = P.panelH || 1150;
  const FLOOR_H = 150, BASE = 1040, NF = P.floors.length;
  const floorTop = i => BASE - (i + 1) * FLOOR_H;
  const SX = 150, SW = 170, CW = 150, CH = 126;
  const panel = el('div', { class: 'abs', style: { left: 0, top: 0, width: W + 'px', height: PH + 'px', overflow: 'hidden' } }, root);
  el('div', { class: 'abs', style: { inset: 0, background: 'radial-gradient(120% 80% at 50% 30%, #1C3049 0%, #142336 55%, #0D1826 100%)' } }, panel);
  el('div', { class: 'abs', style: { left: 0, top: (PH - 2) + 'px', width: W + 'px', height: '2px', background: 'linear-gradient(90deg, transparent, rgba(201,165,95,.55), transparent)' } }, panel);
  const fadeShadow = el('div', { class: 'abs', style: { left: 0, top: PH + 'px', width: W + 'px', height: '60px', background: 'linear-gradient(rgba(0,0,0,.45), rgba(0,0,0,0))' } }, root);
  const hdr = el('div', { class: 'abs kicker', style: { left: 0, width: W + 'px', top: '74px', textAlign: 'center', fontSize: '25px' } }, panel, P.header || 'O elevador do conflito');
  const sub = el('div', { class: 'abs serif', style: { left: '40px', width: (W - 80) + 'px', top: '114px', textAlign: 'center', fontSize: '42px', fontStyle: 'italic', fontWeight: 300, color: PAL.cream } }, panel, P.sub || '');
  const svg = svgEl('svg', { width: W, height: PH, viewBox: `0 0 ${W} ${PH}`, class: 'abs', style: 'left:0;top:0' }, panel);
  const defs = svgEl('defs', {}, svg);
  const gb = svgEl('g', {}, svg);
  const roofY = floorTop(NF - 1);
  const sg = svgEl('linearGradient', { id: 'shaftg', x1: 0, x2: 1, y1: 0, y2: 0 }, defs);
  svgEl('stop', { offset: '0%', 'stop-color': '#070E17' }, sg); svgEl('stop', { offset: '50%', 'stop-color': '#0E1B2B' }, sg); svgEl('stop', { offset: '100%', 'stop-color': '#070E17' }, sg);
  svgEl('rect', { x: 110, y: roofY - 14, width: 860, height: BASE - roofY + 14, fill: 'rgba(245,240,230,.025)' }, gb);
  svgEl('rect', { x: SX, y: roofY - 10, width: SW, height: BASE - roofY + 10, fill: 'url(#shaftg)', stroke: 'rgba(201,165,95,.35)', 'stroke-width': 1.5, rx: 6 }, gb);
  for (const dx of [18, SW - 18]) svgEl('line', { x1: SX + dx, x2: SX + dx, y1: roofY - 6, y2: BASE, stroke: 'rgba(245,240,230,.10)', 'stroke-width': 2 }, gb);
  for (let i = 0; i <= NF; i++) {
    const y = BASE - i * FLOOR_H;
    svgEl('rect', { x: 110, y: y, width: 860, height: 9, fill: i === 0 ? 'rgba(245,240,230,.10)' : 'rgba(0,0,0,.28)' }, gb);
    svgEl('line', { x1: 110, x2: 970, y1: y, y2: y, stroke: i === 0 ? 'rgba(245,240,230,.55)' : 'rgba(245,240,230,.18)', 'stroke-width': i === 0 ? 3 : 1.5 }, gb);
  }
  svgEl('path', { d: `M110 ${roofY} L110 ${roofY - 14} L970 ${roofY - 14} L970 ${roofY}`, fill: 'none', stroke: 'rgba(245,240,230,.25)', 'stroke-width': 1.5 }, gb);
  const lanterns = []; for (let i = 0; i < NF; i++) lanterns.push(svgEl('circle', { cx: SX + SW + 14, cy: floorTop(i) + 22, r: 5, fill: PAL.goldL, opacity: .15 }, gb));
  const cable = svgEl('line', { x1: SX + SW / 2, x2: SX + SW / 2, y1: roofY - 10, y2: BASE, stroke: 'rgba(245,240,230,.35)', 'stroke-width': 2 }, gb);
  // speed lines (accelerator)
  const speed = svgEl('g', { opacity: 0 }, svg);
  for (let k = 0; k < 6; k++) svgEl('line', { x1: SX - 26 - (k % 2) * 10, x2: SX - 26 - (k % 2) * 10, y1: 0, y2: 46 + (k % 3) * 18, stroke: PAL.goldL, 'stroke-width': 3, 'stroke-linecap': 'round', 'data-k': k }, speed);
  // cabin
  const cab = svgEl('g', {}, svg);
  const rg = svgEl('radialGradient', { id: 'orb', cx: '40%', cy: '35%', r: '65%' }, defs);
  svgEl('stop', { offset: '0%', 'stop-color': '#FFF4DC' }, rg);
  const s2 = svgEl('stop', { offset: '55%', 'stop-color': PAL.goldL }, rg);
  const s3 = svgEl('stop', { offset: '100%', 'stop-color': PAL.gold }, rg);
  const glow = svgEl('filter', { id: 'glow', x: '-100%', y: '-100%', width: '300%', height: '300%' }, defs); svgEl('feGaussianBlur', { stdDeviation: 10 }, glow);
  svgEl('rect', { x: 0, y: 0, width: CW, height: CH, rx: 8, fill: '#F3E3BF', 'fill-opacity': .16, stroke: PAL.gold, 'stroke-width': 2.5 }, cab);
  const interior = svgEl('rect', { x: 6, y: 6, width: CW - 12, height: CH - 12, rx: 4, fill: '#F7E7C2', 'fill-opacity': 0 }, cab);
  const orbGlow = svgEl('circle', { cx: CW / 2, cy: CH / 2 + 8, r: 14, fill: PAL.goldL, opacity: .55, filter: 'url(#glow)' }, cab);
  const orb = svgEl('circle', { cx: CW / 2, cy: CH / 2 + 8, r: 14, fill: 'url(#orb)' }, cab);
  const cp = svgEl('clipPath', { id: 'cabclip' }, defs); svgEl('rect', { x: 4, y: 4, width: CW - 8, height: CH - 8 }, cp);
  const doors = svgEl('g', { 'clip-path': 'url(#cabclip)' }, cab);
  const doorL = svgEl('rect', { x: 4, y: 4, width: CW / 2 - 4, height: CH - 8, fill: '#2A4560', 'fill-opacity': .62, stroke: 'rgba(201,165,95,.6)', 'stroke-width': 1 }, doors);
  const doorR = svgEl('rect', { x: CW / 2, y: 4, width: CW / 2 - 4, height: CH - 8, fill: '#2A4560', 'fill-opacity': .62, stroke: 'rgba(201,165,95,.6)', 'stroke-width': 1 }, doors);
  svgEl('path', { d: `M0 0 L12 -10 L${CW + 12} -10 L${CW} 0 Z`, fill: 'rgba(226,200,143,.35)', stroke: 'rgba(201,165,95,.6)', 'stroke-width': 1 }, cab);
  svgEl('path', { d: `M${CW} 0 L${CW + 12} -10 L${CW + 12} ${CH - 10} L${CW} ${CH} Z`, fill: 'rgba(10,18,28,.8)', stroke: 'rgba(201,165,95,.35)', 'stroke-width': 1 }, cab);
  const pulse = svgEl('circle', { cx: CW / 2, cy: CH / 2 + 8, r: 20, fill: 'none', stroke: PAL.goldL, 'stroke-width': 2, opacity: 0 }, cab);
  // indicator
  const ind = el('div', { class: 'abs sans', style: { left: SX + 'px', width: SW + 'px', top: (roofY - 82) + 'px', height: '58px', borderRadius: '10px', background: '#0A121C', border: '1.5px solid rgba(201,165,95,.6)', color: PAL.goldL, font: "700 36px 'Inter Tight'", display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', fontVariantNumeric: 'tabular-nums' } }, panel);
  const indArrow = el('span', { style: { fontSize: '26px', display: 'inline-block' } }, ind, '▲');
  const indNum = el('span', {}, ind, 'T');
  // rows
  const rows = P.floors.map((f, i) => {
    const y = floorTop(i);
    const r = el('div', { class: 'abs', style: { left: '355px', top: (y + 12) + 'px', width: '600px', height: (FLOOR_H - 24) + 'px', opacity: 0 } }, panel);
    el('div', { class: 'abs', style: { left: 0, top: '6px', width: '5px', height: (FLOOR_H - 40) + 'px', borderRadius: '3px', background: [PAL.gold, PAL.tealL, PAL.teal, '#3A5F86', PAL.cream][i] } }, r);
    el('div', { class: 'abs kicker', style: { left: '26px', top: '2px', fontSize: '19px', letterSpacing: '.28em', color: 'rgba(245,240,230,.55)' } }, r, f.level);
    el('div', { class: 'abs serif', style: { left: '24px', top: '24px', fontSize: '46px', fontWeight: 600, color: PAL.white, lineHeight: 1 } }, r, f.name);
    el('div', { class: 'abs sans', style: { left: '26px', top: '78px', fontSize: '24px', fontWeight: 500, color: 'rgba(245,240,230,.74)', width: '420px', lineHeight: 1.18 } }, r, f.desc || '');
    const brake = el('div', { class: 'abs sans', style: { right: '0px', top: '28px', padding: '8px 14px', borderRadius: '999px', border: '1.5px solid rgba(200,100,75,.9)', background: 'rgba(200,100,75,.12)', color: '#F2B3A3', font: "600 19px 'Inter Tight'", letterSpacing: '.14em', opacity: 0 } }, r, '✕ SEM FREIO');
    return { r, brake };
  });
  const pill = el('div', { class: 'abs sans', style: { left: (SX + SW + 30) + 'px', top: '0px', padding: '14px 24px', borderRadius: '14px', background: 'rgba(28,46,70,.96)', border: '1.5px solid rgba(226,200,143,.85)', color: PAL.white, font: "650 36px 'Inter Tight'", opacity: 0, whiteSpace: 'nowrap', boxShadow: '0 10px 30px rgba(0,0,0,.45)' } }, panel);
  const note = P.topNote ? el('div', { class: 'abs sans', style: { right: '110px', top: (roofY - 66) + 'px', padding: '10px 18px', borderRadius: '12px', background: 'rgba(200,100,75,.18)', border: '1.5px solid rgba(240,168,147,.85)', color: '#FFE3DA', font: "650 23px 'Inter Tight'", opacity: 0, whiteSpace: 'nowrap' } }, panel, P.topNote.text) : null;
  const accel = P.accel ? el('div', { class: 'abs', style: { left: '60px', width: '960px', top: (PH - 104) + 'px', textAlign: 'center', opacity: 0 } }, panel) : null;
  let acc1, acc2;
  if (accel) { acc1 = el('span', { class: 'sans', style: { font: "600 30px 'Inter Tight'", color: 'rgba(245,240,230,.85)' } }, accel, P.accel.text + ' '); acc2 = el('span', { class: 'serif', style: { fontSize: '42px', fontStyle: 'italic', color: PAL.goldL, opacity: 0 } }, accel, P.accel.text2 || ''); }
  const closing = P.closing ? el('div', { class: 'abs serif', style: { left: '60px', width: '960px', top: (PH - 96) + 'px', textAlign: 'center', fontSize: '38px', fontStyle: 'italic', color: PAL.goldL, opacity: 0 } }, panel, P.closing) : null;

  const MOVE = 1.25, DOOR = .45;
  const stops = (P.stops && P.stops.length) ? P.stops : P.floors.map((f, i) => ({ t: f.t, floor: i }));
  const start = P.startFloor ?? stops[0]?.floor ?? 0;
  function floorPos(t) {
    let pos = start, prevF = start;
    for (const s of stops) {
      if (t >= s.t) { pos = s.floor; prevF = s.floor; continue; }
      if (t > s.t - MOVE) return lerp(prevF, s.floor, E.inOutCubic(clamp((t - (s.t - MOVE)) / MOVE)));
      return prevF;
    }
    return pos;
  }
  return t => {
    const a = env(t, 0, P.dur, .7, .6, E.outQuart, E.inOutCubic);
    panel.style.opacity = Math.min(1, a * 1.4); fadeShadow.style.opacity = a;
    panel.style.transform = `translateY(${(1 - E.outQuart(clamp(t / .8))) * -40}px)`;
    rise(hdr, prog(t, .25, .7), 18, 6); rise(sub, prog(t, P.subAt ?? .45, .8), 18, 6);
    const pos = floorPos(t), pi = Math.round(pos);
    // accelerator: shake the cabin slightly + speed lines
    const ak = P.accel ? prog(t, P.accel.t, .5) : 0;
    const shake = ak ? Math.sin(t * 60) * 2.2 * ak : 0;
    const y = BASE - pos * FLOOR_H - FLOOR_H + (FLOOR_H - CH) - 6;
    cab.setAttribute('transform', `translate(${SX + (SW - CW) / 2 + shake}, ${y})`);
    cable.setAttribute('y2', y);
    speed.setAttribute('opacity', ak * .9);
    speed.querySelectorAll('line').forEach((ln, k) => { const yy = y + ((t * 420 + k * 37) % (CH + 40)) - 20; ln.setAttribute('y1', yy); ln.setAttribute('y2', yy + 30 + (k % 3) * 14); ln.setAttribute('x1', SX - 22 - (k % 3) * 12); ln.setAttribute('x2', SX - 22 - (k % 3) * 12); });
    // doors: open while parked at a stop (after its arrival), closed while moving
    let open = 0;
    for (let k = 0; k < stops.length; k++) {
      const ta = stops[k].t, tl = (k + 1 < stops.length ? stops[k + 1].t - MOVE : 1e9);
      if (t >= ta && t < tl) open = Math.min(E.outCubic(clamp((t - ta) / DOOR)), 1 - E.inOutCubic(clamp((t - (tl - DOOR)) / DOOR)));
    }
    if (!stops.length) open = .35;
    doorL.setAttribute('x', 4 - open * (CW / 2 - 8)); doorR.setAttribute('x', CW / 2 + open * (CW / 2 - 8));
    interior.setAttribute('fill-opacity', .10 + .22 * open);
    lanterns.forEach((L, i) => { const on = (Math.abs(pos - i) < .03) ? Math.max(.15, open) : .15; L.setAttribute('opacity', on); });
    let lastArr = -1e9; for (const s of stops) if (t >= s.t) lastArr = s.t;
    const pk = clamp((t - lastArr) / .9);
    pulse.setAttribute('opacity', lastArr > -1e8 ? (1 - pk) * .8 : 0); pulse.setAttribute('r', 18 + pk * 40);
    const grow = clamp(pos / (NF - 1));
    const r = 13 + 26 * grow; orb.setAttribute('r', r); orbGlow.setAttribute('r', r * 1.15);
    s2.setAttribute('stop-color', grow < .5 ? PAL.goldL : '#D98B66'); s3.setAttribute('stop-color', grow < .5 ? PAL.gold : PAL.red); orbGlow.setAttribute('fill', grow < .5 ? PAL.goldL : PAL.red);
    indNum.textContent = pi === 0 ? 'T' : String(pi);
    const moving = Math.abs(pos - pi) > .02;
    indArrow.style.opacity = moving ? (0.55 + .45 * Math.abs(Math.sin(t * 6))) : .35;
    rows.forEach((R, i) => {
      const shown = prog(t, P.floors[i].t - .25, .6);
      let op;
      if (P.rowsDim) op = shown * (Math.abs(pos - i) < .5 ? .5 : .25);
      else { const active = Math.abs(pos - i) < .5; op = shown * (active ? 1 : .55); }
      if (P.freio != null && t >= P.freio) op = Math.max(op, shown * .85);
      R.r.style.opacity = op; R.r.style.transform = `translateX(${(1 - shown) * 24}px)`;
      const bk = P.freio != null ? prog(t, P.freio + i * .3, .45) : 0;
      R.brake.style.opacity = bk; R.brake.style.transform = `scale(${.9 + .1 * bk})`;
    });
    if (P.pills) {
      let txt = null, ta = 0;
      P.pills.forEach(pp => { if (t >= pp.t - .15) { txt = pp.text; ta = pp.t; } });
      if (txt) { pill.textContent = txt; const k = prog(t, ta - .15, .45); pill.style.opacity = k; pill.style.top = (y + CH / 2 - 36) + 'px'; pill.style.transform = `translateX(${(1 - k) * -18}px)`; }
      else pill.style.opacity = 0;
    }
    if (note) { const k = prog(t, P.topNote.t, .5); note.style.opacity = k; note.style.transform = `translateY(${(1 - k) * 10}px)`; }
    if (accel) { accel.style.opacity = prog(t, P.accel.t, .5); acc2.style.opacity = prog(t, P.accel.t2 ?? P.accel.t + 1, .5); }
    if (closing) rise(closing, prog(t, P.closingAt ?? 1e9, .8), 16, 6);
  };
};
