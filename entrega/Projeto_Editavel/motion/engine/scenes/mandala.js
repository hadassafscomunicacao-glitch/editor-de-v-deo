// Mandala do Método Cultura em Ação: 4 concentric rings painted from the inside out.
// params: dur, panelH, tMarket (market paints outside-in -> fails), tInside (start inside-out), rings:[t_diag,t_estr,t_impl,t_lid], deps:[{t, from, to}], tFinal
SCENES.mandala = (root, P) => {
  const W = 1080, PH = P.panelH || 1150, CX = 540, CY = 640;
  const panel = el('div', { class: 'abs', style: { left: 0, top: 0, width: W + 'px', height: PH + 'px', overflow: 'hidden' } }, root);
  el('div', { class: 'abs', style: { inset: 0, background: 'radial-gradient(90% 70% at 50% 52%, #1F3550 0%, #142336 55%, #0C1724 100%)' } }, panel);
  el('div', { class: 'abs', style: { left: 0, top: (PH - 2) + 'px', width: W + 'px', height: '2px', background: 'linear-gradient(90deg, transparent, rgba(201,165,95,.55), transparent)' } }, panel);
  const shadow = el('div', { class: 'abs', style: { left: 0, top: PH + 'px', width: W + 'px', height: '60px', background: 'linear-gradient(rgba(0,0,0,.45), rgba(0,0,0,0))' } }, root);
  const kick = el('div', { class: 'abs kicker', style: { left: 0, width: W + 'px', top: '74px', textAlign: 'center', fontSize: '24px' } }, panel, P.kicker || 'Método Cultura em Ação');
  const ttl = el('div', { class: 'abs serif', style: { left: 0, width: W + 'px', top: '112px', textAlign: 'center', fontSize: '50px', fontStyle: 'italic', fontWeight: 300, color: PAL.cream } }, panel, P.title || 'a mandala se pinta de dentro para fora');
  const svg = svgEl('svg', { width: W, height: PH, class: 'abs', style: 'left:0;top:0' }, panel);
  const R = [150, 250, 345, 430];
  const COL = [PAL.gold, '#1B2D44', PAL.teal, '#EDE6D8'];
  const TXT = ['#1A1A1A', '#FFFFFF', '#FFFFFF', '#142336'];
  const NAMES = ['DIAGNÓSTICO', 'ESTRUTURA', 'IMPLEMENTAÇÃO', 'LIDERANÇA'];
  const SUBS = P.subs || ['escutar antes de agir', 'regra escrita', 'apresentada, aplicada', 'líder preparado'];
  // ghost outline of the full mandala
  const ghost = R.map(r => svgEl('circle', { cx: CX, cy: CY, r, fill: 'none', stroke: 'rgba(245,240,230,.16)', 'stroke-width': 1.5, 'stroke-dasharray': '4 8' }, svg));
  // painted rings: draw from outer to inner so inner sits on top
  const rings = [];
  const RIN = [0, R[0], R[1], R[2]];
  for (let i = 3; i >= 0; i--) {
    if (i === 0) rings[i] = svgEl('circle', { cx: CX, cy: CY, r: R[0], fill: COL[0], opacity: 0 }, svg);
    else rings[i] = svgEl('circle', { cx: CX, cy: CY, r: (R[i] + RIN[i]) / 2, fill: 'none', stroke: COL[i], 'stroke-width': R[i] - RIN[i] + 1, opacity: 0 }, svg);
  }
  // labels at the top of each ring band
  const labels = NAMES.map((n, i) => {
    const yTop = CY - R[i] + (i === 0 ? 120 : 40);
    const g = el('div', { class: 'abs', style: { left: (CX - 260) + 'px', width: '520px', top: (i === 0 ? CY - 32 : yTop - 22) + 'px', textAlign: 'center', opacity: 0 } }, panel);
    el('div', { style: { font: "500 16px 'Fraunces'", color: i === 0 ? '#6B5426' : PAL.goldL, letterSpacing: '.2em' } }, g, '0' + (i + 1));
    el('div', { style: { font: `600 ${i === 0 ? 34 : 30}px 'Fraunces'`, letterSpacing: '.12em', color: TXT[i] } }, g, n);
    el('div', { style: { font: "500 18px 'Inter Tight'", color: i === 0 ? 'rgba(26,26,26,.75)' : (i === 3 ? 'rgba(20,35,54,.7)' : 'rgba(255,255,255,.72)'), marginTop: '4px' } }, g, SUBS[i]);
    return g;
  });
  // market attempt: outer ring painted first, then it "has nothing underneath" and falls away
  const mk = el('div', { class: 'abs sans', style: { left: 0, width: W + 'px', top: (CY + R[3] + 26) + 'px', textAlign: 'center', font: "600 30px 'Inter Tight'", color: '#F0A893', opacity: 0, textShadow: '0 2px 10px rgba(0,0,0,.5)' } }, panel, P.marketText || '✕  o mercado pinta de fora para dentro');
  const ok = el('div', { class: 'abs sans', style: { left: 0, width: W + 'px', top: (CY + R[3] + 26) + 'px', textAlign: 'center', font: "600 30px 'Inter Tight'", color: '#BFE3D8', opacity: 0, textShadow: '0 2px 10px rgba(0,0,0,.5)' } }, panel, P.okText || '✓  de dentro para fora');
  const arrowsIn = [0, 1, 2, 3].map(k => {
    const ang = Math.PI / 4 + k * Math.PI / 2;
    const x1 = CX + Math.cos(ang) * (R[3] + 70), y1 = CY + Math.sin(ang) * (R[3] + 70);
    const x2 = CX + Math.cos(ang) * (R[3] + 8), y2 = CY + Math.sin(ang) * (R[3] + 8);
    return svgEl('line', { x1, y1, x2, y2, stroke: '#F0A893', 'stroke-width': 3, 'stroke-linecap': 'round', opacity: 0, 'marker-end': 'url(#ah)' }, svg);
  });
  const defs = svgEl('defs', {}, svg);
  const mkr = svgEl('marker', { id: 'ah', markerWidth: 10, markerHeight: 10, refX: 6, refY: 5, orient: 'auto' }, defs);
  svgEl('path', { d: 'M0,0 L10,5 L0,10 z', fill: '#F0A893' }, mkr);
  // radial "inside-out" pulse
  const pulse = svgEl('circle', { cx: CX, cy: CY, r: 10, fill: 'none', stroke: PAL.goldL, 'stroke-width': 2.5, opacity: 0 }, svg);
  const deps = (P.deps || []).map(d => ({ d, e: el('div', { class: 'abs sans', style: { left: 0, width: W + 'px', top: (CY + R[3] + 26) + 'px', textAlign: 'center', font: "600 30px 'Inter Tight'", color: '#fff', opacity: 0, textShadow: '0 2px 10px rgba(0,0,0,.5)' } }, panel, d.text) }));
  return t => {
    const a = env(t, 0, P.dur, .7, .6, E.outQuart, E.inOutCubic);
    panel.style.opacity = Math.min(1, a * 1.4); shadow.style.opacity = a;
    rise(kick, prog(t, .2, .6), 14, 4); rise(ttl, prog(t, .4, .8), 16, 6);
    ghost.forEach((g, i) => g.setAttribute('opacity', prog(t, .3 + i * .08, .6)));
    // market phase
    let marketK = 0, marketFall = 0;
    if (P.tMarket != null) {
      marketK = prog(t, P.tMarket, .8, E.outCubic);
      marketFall = P.tInside != null ? prog(t, P.tInside - .9, .8, E.inOutCubic) : 0;
      arrowsIn.forEach((ar, k) => ar.setAttribute('opacity', marketK * (1 - marketFall) * prog(t, P.tMarket + k * .08, .4)));
      mk.style.opacity = marketK * (1 - marketFall);
    }
    // inside-out painting
    const RT = P.rings || [];
    for (let i = 0; i < 4; i++) {
      let op = 0, scale = 1;
      if (RT[i] != null && t >= RT[i] - .05) { const k = prog(t, RT[i], .75, E.outCubic); op = k; scale = .9 + .1 * k; }
      if (i === 3 && P.tMarket != null && (RT[3] == null || t < RT[3])) {
        // outer ring painted alone by "the market", wobbles and fades away (nothing underneath)
        op = Math.max(op, marketK * .85 * (1 - marketFall));
        scale = 1 + .05 * marketFall;
      }
      rings[i].setAttribute('opacity', op);
      if (i === 0) rings[i].setAttribute('r', R[0] * scale); else rings[i].setAttribute('r', ((R[i] + RIN[i]) / 2) * scale);
      const lk = RT[i] != null ? prog(t, RT[i] + .25, .6) : 0;
      labels[i].style.opacity = lk; labels[i].style.transform = `translateY(${(1 - lk) * 10}px)`;
    }
    if (RT[0] != null) {
      const pk = clamp((t - RT[0]) / 1.4);
      pulse.setAttribute('opacity', t >= RT[0] && pk < 1 ? (1 - pk) * .9 : 0); pulse.setAttribute('r', 20 + pk * 430);
      ok.style.opacity = prog(t, RT[0] + .3, .6) * (deps.some(x => t >= x.d.t) ? 0 : 1);
    }
    deps.forEach(({ d, e }, k) => { const on = t >= d.t && (k + 1 >= deps.length || t < deps[k + 1].t); e.style.opacity = on ? prog(t, d.t, .45) : 0; });
  };
};
