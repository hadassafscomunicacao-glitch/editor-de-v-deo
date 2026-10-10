// ---------- Bespoke illustrative scenes (top zone unless noted). Times relative to scene start.
function panelBox(parent, x, y, w, h, extra = {}) {
  return el('div', { class: 'abs', style: Object.assign({ left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px', borderRadius: '26px', background: 'linear-gradient(160deg, rgba(31,52,78,.94), rgba(17,30,46,.94))', border: '1.5px solid rgba(201,165,95,.45)', boxShadow: '0 24px 60px rgba(0,0,0,.45)' }, extra) }, parent);
}
function exitK(t, P) { return 1 - E.inOutCubic(clamp((t - (P.out ?? P.dur - .55)) / .5)); }

// DATA CARD: big number counting up. P.prefix, P.value, P.decimals, P.suffix, P.label, P.sub, P.top, P.tCount, P.from
SCENES.dataCard = (root, P) => {
  const box = el('div', { class: 'abs', style: { left: '70px', width: '940px', top: (P.top ?? 175) + 'px', textAlign: 'center' } }, root);
  const kick = P.kicker ? el('div', { class: 'kicker', style: { fontSize: '23px', marginBottom: '10px' } }, box, P.kicker) : null;
  const num = el('div', { class: 'shadow', style: { font: `700 ${P.size || 150}px 'Inter Tight'`, color: '#fff', letterSpacing: '-0.035em', lineHeight: 1, fontVariantNumeric: 'tabular-nums' } }, box);
  const lab = el('div', { class: 'serif shadow', style: { fontSize: (P.labelSize || 46) + 'px', fontStyle: 'italic', color: PAL.goldL, marginTop: '12px', lineHeight: 1.1 } }, box, P.label || '');
  const sub = P.sub ? el('div', { class: 'sans shadow', style: { font: "500 28px 'Inter Tight'", color: 'rgba(245,240,230,.85)', marginTop: '14px', lineHeight: 1.25 } }, box, P.sub) : null;
  const fmt = v => {
    const s = v.toFixed(P.decimals || 0).replace('.', ',');
    const parts = s.split(','); parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    return (P.prefix || '') + parts.join(',') + (P.suffix || '');
  };
  return t => {
    const ex = exitK(t, P);
    if (kick) rise(kick, prog(t, 0, .5) * ex, 12, 4);
    const a = prog(t, .1, .55) * ex; rise(num, a, 24, 8);
    const k = prog(t, P.tCount ?? .15, P.countDur ?? 1.3, E.outQuart);
    num.innerHTML = fmt((P.from ?? 0) + (P.value - (P.from ?? 0)) * k) + (P.unit ? `<span style="font-size:.42em;font-weight:600;letter-spacing:0;margin-left:.18em">${P.unit}</span>` : '');
    rise(lab, prog(t, P.tLabel ?? .5, .6) * ex, 16, 6);
    if (sub) rise(sub, prog(t, P.tSub ?? .9, .6) * ex, 12, 4);
  };
};

// FROM -> TO comparison of two numbers (e.g. burnout: menos de mil -> 5 mil). P.a {text,label}, P.b {text,label}, P.tB
SCENES.fromTo = (root, P) => {
  const box = el('div', { class: 'abs', style: { left: '70px', width: '940px', top: (P.top ?? 180) + 'px' } }, root);
  const kick = P.kicker ? el('div', { class: 'kicker', style: { textAlign: 'center', fontSize: '23px', marginBottom: '22px' } }, box, P.kicker) : null;
  const row = el('div', { style: { display: 'flex', alignItems: 'flex-end', justifyContent: 'center', gap: '40px' } }, box);
  const mk = (c, big) => {
    const col = el('div', { style: { textAlign: 'center' } }, row);
    const n = el('div', { class: 'shadow', style: { font: `700 ${big ? 120 : 84}px 'Inter Tight'`, color: big ? '#fff' : 'rgba(255,255,255,.7)', letterSpacing: '-0.03em', lineHeight: 1 } }, col, c.text);
    const l = el('div', { class: 'sans', style: { font: "600 24px 'Inter Tight'", letterSpacing: '.16em', textTransform: 'uppercase', color: PAL.goldL, marginTop: '12px', textShadow: '0 2px 10px rgba(0,0,0,.6)' } }, col, c.label);
    return col;
  };
  const A = mk(P.a, false);
  const arrow = el('div', { class: 'serif', style: { fontSize: '90px', color: PAL.gold, lineHeight: 1, paddingBottom: '40px' } }, row, '→');
  const B = mk(P.b, true);
  const cap = P.caption ? el('div', { class: 'serif shadow', style: { textAlign: 'center', fontSize: '44px', fontStyle: 'italic', color: PAL.goldL, marginTop: '20px' } }, box, P.caption) : null;
  return t => {
    const ex = exitK(t, P);
    if (kick) rise(kick, prog(t, 0, .5) * ex, 12, 4);
    rise(A, prog(t, .1, .6) * ex, 20, 6);
    const ak = prog(t, (P.tB ?? 1.2) - .4, .5) * ex; arrow.style.opacity = ak; arrow.style.transform = `translateX(${(1 - ak) * -20}px)`;
    rise(B, prog(t, P.tB ?? 1.2, .7) * ex, 28, 8);
    if (cap) rise(cap, prog(t, P.tCap ?? 2, .6) * ex, 14, 5);
  };
};

// AWARENESS CURVE (training spike that fades over months). Conceptual, no numbers. P.tEvent, P.tDecay, P.tLabel2
SCENES.curve = (root, P) => {
  const X0 = 120, X1 = 960, Y0 = 560, Y1 = 250;
  const kick = el('div', { class: 'abs kicker', style: { left: 0, width: '1080px', textAlign: 'center', top: '150px', fontSize: '23px' } }, root, P.kicker || 'Consciência depois do treinamento');
  const svg = svgEl('svg', { width: 1080, height: 700, class: 'abs', style: 'left:0;top:0;overflow:visible' }, root);
  const defs = svgEl('defs', {}, svg);
  const lg = svgEl('linearGradient', { id: 'cg', x1: 0, x2: 0, y1: 0, y2: 1 }, defs);
  svgEl('stop', { offset: '0%', 'stop-color': PAL.goldL, 'stop-opacity': .45 }, lg); svgEl('stop', { offset: '100%', 'stop-color': PAL.goldL, 'stop-opacity': 0 }, lg);
  const axis = svgEl('line', { x1: X0, x2: X1, y1: Y0, y2: Y0, stroke: 'rgba(255,255,255,.5)', 'stroke-width': 2 }, svg);
  // curve: flat baseline, sharp rise at the event, slow decay back to baseline
  const pts = [];
  for (let i = 0; i <= 200; i++) {
    const u = i / 200, x = X0 + (X1 - X0) * u;
    let v = .12;
    if (u > .22) { const d = u - .22; v = .12 + .78 * (1 - Math.exp(-d * 60)) * Math.exp(-d * 4.2); }
    pts.push([x, Y0 - (Y0 - Y1) * v]);
  }
  const path = svgEl('path', { d: 'M' + pts.map(p => p.join(',')).join(' L'), fill: 'none', stroke: PAL.goldL, 'stroke-width': 5, 'stroke-linecap': 'round' }, svg);
  const area = svgEl('path', { d: 'M' + pts.map(p => p.join(',')).join(' L') + ` L${X1},${Y0} L${X0},${Y0} Z`, fill: 'url(#cg)' }, svg);
  const L = path.getTotalLength(); path.setAttribute('stroke-dasharray', L);
  const dot = svgEl('circle', { r: 9, fill: '#fff' }, svg);
  const lbl = (txt, x, y, al) => el('div', { class: 'abs sans shadow', style: { left: (al === 'r' ? x - 400 : x) + 'px', width: '400px', textAlign: al === 'r' ? 'right' : 'left', top: y + 'px', font: "600 28px 'Inter Tight'", color: '#fff', opacity: 0 } }, root, txt);
  const l1 = lbl(P.label1 || 'palestra / workshop', X0 + (X1 - X0) * .24 + 14, Y1 - 6, 'l');
  const l2 = lbl(P.label2 || 'alguns meses depois', X1, Y0 + 18, 'r');
  const l3 = P.label3 ? el('div', { class: 'abs serif shadow', style: { left: 0, width: '1080px', textAlign: 'center', top: (Y0 + 70) + 'px', fontSize: '46px', fontStyle: 'italic', color: PAL.goldL, opacity: 0 } }, root, P.label3) : null;
  return t => {
    const ex = exitK(t, P);
    rise(kick, prog(t, 0, .5) * ex, 12, 4);
    axis.setAttribute('opacity', prog(t, .1, .5) * ex);
    // draw progress: to the peak at tEvent, then decay draws until tDecay+2
    const d1 = prog(t, .3, Math.max(.4, (P.tEvent ?? 1.2) - .3), E.inOutCubic) * .3;
    const d2 = prog(t, P.tDecay ?? 3, 2.4, E.inOutSine) * .7;
    const frac = d1 + d2;
    path.setAttribute('stroke-dashoffset', L * (1 - frac)); path.setAttribute('opacity', ex);
    area.setAttribute('opacity', ex * Math.min(1, frac * 1.4) * .8);
    const pt = path.getPointAtLength(L * frac); dot.setAttribute('cx', pt.x); dot.setAttribute('cy', pt.y); dot.setAttribute('opacity', ex * (frac > .01 ? 1 : 0));
    l1.style.opacity = prog(t, (P.tEvent ?? 1.2), .5) * ex;
    l2.style.opacity = prog(t, (P.tDecay ?? 3) + 1.6, .6) * ex;
    if (l3) rise(l3, prog(t, P.tLabel3 ?? 5, .6) * ex, 14, 5);
  };
};

// DOCUMENTS INTO A DRAWER. P.docs [{text,t}], P.tDrawer
SCENES.drawer = (root, P) => {
  const kick = el('div', { class: 'abs kicker', style: { left: 0, width: '1080px', textAlign: 'center', top: '140px', fontSize: '23px' } }, root, P.kicker || 'A parte normativa');
  const docs = P.docs.map((d, i) => {
    const e = el('div', { class: 'abs', style: { left: '290px', width: '500px', height: '52px', top: (195 + i * 60) + 'px', borderRadius: '10px', background: '#F5F0E6', boxShadow: '0 10px 24px rgba(0,0,0,.35)', display: 'flex', alignItems: 'center', gap: '16px', padding: '0 22px', boxSizing: 'border-box', font: "600 27px 'Inter Tight'", color: '#142336' } }, root);
    el('div', { style: { width: '26px', height: '32px', borderRadius: '3px', background: PAL.teal, flex: '0 0 auto', boxShadow: 'inset -6px -6px 0 rgba(0,0,0,.12)' } }, e);
    el('span', {}, e, d.text);
    return { e, d, i };
  });
  // drawer (front face) below
  const DY = 195 + P.docs.length * 60 + 16;
  const drawer = el('div', { class: 'abs', style: { left: '240px', width: '600px', top: DY + 'px', height: '96px', borderRadius: '14px', background: 'linear-gradient(#2A3E57,#1B2A3D)', border: '2px solid rgba(201,165,95,.55)', boxShadow: '0 20px 50px rgba(0,0,0,.5)', opacity: 0 } }, root);
  el('div', { class: 'abs', style: { left: '250px', top: '40px', width: '100px', height: '14px', borderRadius: '7px', background: PAL.gold } }, drawer);
  const cap = el('div', { class: 'abs serif shadow', style: { left: 0, width: '1080px', textAlign: 'center', top: '250px', fontSize: '58px', fontStyle: 'italic', color: PAL.goldL, opacity: 0 } }, root, P.caption || '…e guarda numa gaveta.');
  return t => {
    const ex = exitK(t, P);
    rise(kick, prog(t, 0, .5) * ex, 12, 4);
    const td = P.tDrawer ?? 4;
    const dk = prog(t, td - .5, .6);
    drawer.style.opacity = dk * ex; drawer.style.transform = `translateY(${(1 - dk) * 30}px)`;
    docs.forEach(({ e, d, i }) => {
      const a = prog(t, d.t, .5);
      const fall = prog(t, td + .15 + (docs.length - 1 - i) * .09, .55, E.inCubic);
      const y = (1 - a) * 24 + fall * (DY + 30 - (195 + i * 60));
      e.style.opacity = a * ex * (1 - fall * .95);
      e.style.transform = `translateY(${y}px) scale(${1 - fall * .25})`;
    });
    rise(cap, prog(t, td + .9, .6) * ex, 14, 5);
    kick.style.opacity = Math.min(+kick.style.opacity, 1 - prog(t, td + .6, .4));
  };
};

// LOOP between two sides (Hellen <-> Indira). P.left {title,sub,t}, P.right {...}, P.tTop, P.tBottom, P.topText, P.bottomText
SCENES.loop = (root, P) => {
  const CY = P.cy ?? 400;
  const mkNode = (x, c) => {
    const n = el('div', { class: 'abs', style: { left: (x - 170) + 'px', width: '340px', top: (CY - 80) + 'px', textAlign: 'center' } }, root);
    el('div', { class: 'kicker', style: { fontSize: '19px', marginBottom: '8px' } }, n, c.kicker || '');
    el('div', { class: 'serif shadow', style: { fontSize: '56px', color: '#fff', lineHeight: 1 } }, n, c.title);
    if (c.sub) el('div', { class: 'sans shadow', style: { font: "500 24px 'Inter Tight'", color: 'rgba(245,240,230,.8)', marginTop: '8px' } }, n, c.sub);
    return n;
  };
  const L = mkNode(270, P.left), R = mkNode(810, P.right);
  const svg = svgEl('svg', { width: 1080, height: 800, class: 'abs', style: 'left:0;top:0' }, root);
  const defs = svgEl('defs', {}, svg);
  const mk = svgEl('marker', { id: 'lh', markerWidth: 12, markerHeight: 12, refX: 7, refY: 6, orient: 'auto' }, defs); svgEl('path', { d: 'M0,0 L12,6 L0,12 z', fill: PAL.gold }, mk);
  const dTop = P.reverse ? `M 700 ${CY - 100} Q 540 ${CY - 230} 380 ${CY - 100}` : `M 380 ${CY - 100} Q 540 ${CY - 230} 700 ${CY - 100}`;
  const dBot = P.reverse ? `M 380 ${CY + 110} Q 540 ${CY + 240} 700 ${CY + 110}` : `M 700 ${CY + 110} Q 540 ${CY + 240} 380 ${CY + 110}`;
  const top = svgEl('path', { d: dTop, fill: 'none', stroke: PAL.gold, 'stroke-width': 4, 'marker-end': 'url(#lh)' }, svg);
  const bot = svgEl('path', { d: dBot, fill: 'none', stroke: PAL.gold, 'stroke-width': 4, 'marker-end': 'url(#lh)' }, svg);
  [top, bot].forEach(p => { const l = p.getTotalLength(); p.setAttribute('stroke-dasharray', l); p.dataset.l = l; });
  const tt = el('div', { class: 'abs sans shadow', style: { left: '190px', width: '700px', textAlign: 'center', top: (CY - 250) + 'px', font: "600 30px 'Inter Tight'", color: '#fff', opacity: 0 } }, root, P.topText || '');
  const bt = el('div', { class: 'abs sans shadow', style: { left: '190px', width: '700px', textAlign: 'center', top: (CY + 200) + 'px', font: "600 30px 'Inter Tight'", color: '#fff', opacity: 0 } }, root, P.bottomText || '');
  return t => {
    const ex = exitK(t, P);
    rise(L, prog(t, P.left.t ?? 0, .6) * ex, 18, 6); rise(R, prog(t, P.right.t ?? .3, .6) * ex, 18, 6);
    const k1 = prog(t, P.tTop ?? 1, .9, E.inOutCubic), k2 = prog(t, P.tBottom ?? 2.5, .9, E.inOutCubic);
    top.setAttribute('stroke-dashoffset', top.dataset.l * (1 - k1)); top.setAttribute('opacity', ex);
    bot.setAttribute('stroke-dashoffset', bot.dataset.l * (1 - k2)); bot.setAttribute('opacity', ex);
    rise(tt, prog(t, (P.tTop ?? 1) + .3, .6) * ex, 10, 4); rise(bt, prog(t, (P.tBottom ?? 2.5) + .3, .6) * ex, 10, 4);
  };
};

// FOUR STEPS row: P.tSteps[4], P.tMarket (highlight 04 as where the market starts), P.marketText
SCENES.steps4 = (root, P) => {
  const names = ['Diagnóstico', 'Estrutura', 'Implementação', 'Liderança'];
  const kick = el('div', { class: 'abs kicker', style: { left: 0, width: '1080px', textAlign: 'center', top: '150px', fontSize: '23px' } }, root, P.kicker || 'O método · quatro etapas');
  const items = names.map((n, i) => {
    const x = 70 + i * 240;
    const c = el('div', { class: 'abs', style: { left: x + 'px', width: '220px', top: '215px', textAlign: 'center' } }, root);
    const circ = el('div', { style: { width: '92px', height: '92px', borderRadius: '50%', margin: '0 auto', border: `2.5px solid ${PAL.gold}`, display: 'flex', alignItems: 'center', justifyContent: 'center', font: "italic 400 44px 'Fraunces'", color: PAL.goldL, background: 'rgba(20,35,54,.55)' } }, c, '0' + (i + 1));
    const tx = el('div', { class: 'shadow', style: { font: "650 30px 'Inter Tight'", color: '#fff', marginTop: '16px' } }, c, n);
    return { c, circ, tx, i };
  });
  const conns = [0, 1, 2].map(i => el('div', { class: 'abs', style: { left: (70 + i * 240 + 156) + 'px', top: '260px', height: '2.5px', width: '0px', background: PAL.gold } }, root));
  const mkt = el('div', { class: 'abs sans shadow', style: { left: '470px', width: '560px', textAlign: 'right', top: '400px', font: "600 28px 'Inter Tight'", color: '#F0A893', opacity: 0 } }, root, P.marketText || '↑ o mercado começa por aqui');
  const cap = P.caption ? el('div', { class: 'abs serif shadow', style: { left: 0, width: '1080px', textAlign: 'center', top: '470px', fontSize: '46px', fontStyle: 'italic', color: PAL.goldL, opacity: 0 } }, root, P.caption) : null;
  return t => {
    const ex = exitK(t, P);
    rise(kick, prog(t, 0, .5) * ex, 12, 4);
    items.forEach(({ c, circ, i }) => {
      const k = prog(t, P.tSteps[i], .55); rise(c, k * ex, 22, 6);
      const hot = P.tMarket != null && t >= P.tMarket && i === 3;
      circ.style.borderColor = hot ? '#F0A893' : PAL.gold; circ.style.color = hot ? '#F0A893' : PAL.goldL;
      if (P.tMarket != null && t >= P.tMarket && i < 3) c.style.opacity = Math.min(+c.style.opacity, .45);
    });
    conns.forEach((cn, i) => { cn.style.width = (84 * prog(t, P.tSteps[i + 1] - .2, .4)) + 'px'; cn.style.opacity = ex; });
    if (P.tMarket != null) rise(mkt, prog(t, P.tMarket, .5) * ex, 12, 4);
    if (cap) rise(cap, prog(t, P.tCap ?? 99, .6) * ex, 12, 4);
  };
};

// QUESTION CARD (quiz). P.n, P.step, P.q (html), P.q2 (optional follow-up), P.tQ2
SCENES.question = (root, P) => {
  const card = panelBox(root, 80, P.top ?? 150, 920, P.h ?? 430);
  const head = el('div', { class: 'abs', style: { left: '48px', top: '38px', right: '48px', display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' } }, card);
  el('div', { class: 'kicker', style: { fontSize: '22px' } }, head, `Pergunta ${P.n} de 4`);
  el('div', { style: { font: "600 20px 'Inter Tight'", letterSpacing: '.18em', textTransform: 'uppercase', color: 'rgba(245,240,230,.6)' } }, head, P.step);
  const q = el('div', { class: 'abs serif', style: { left: '48px', right: '48px', top: '100px', fontSize: (P.size || 50) + 'px', color: '#fff', lineHeight: 1.16 } }, card, P.q);
  const q2 = P.q2 ? el('div', { class: 'abs sans', style: { left: '48px', right: '48px', bottom: '96px', font: "500 32px 'Inter Tight'", color: PAL.goldL, lineHeight: 1.2 } }, card, P.q2) : null;
  const yn = el('div', { class: 'abs', style: { left: '48px', bottom: '34px', display: 'flex', gap: '16px' } }, card);
  const chips = ['Sim', 'Não'].map(s => el('div', { style: { padding: '8px 26px', borderRadius: '999px', border: '1.5px solid rgba(245,240,230,.4)', font: "600 22px 'Inter Tight'", color: 'rgba(245,240,230,.85)', letterSpacing: '.08em' } }, yn, s));
  const dots = el('div', { class: 'abs', style: { right: '48px', bottom: '44px', display: 'flex', gap: '10px' } }, card);
  [1, 2, 3, 4].forEach(k => el('div', { style: { width: '34px', height: '5px', borderRadius: '3px', background: k <= P.n ? PAL.goldL : 'rgba(255,255,255,.2)' } }, dots));
  return t => {
    const ex = exitK(t, P);
    const a = prog(t, 0, .6, E.outQuart) * ex;
    card.style.opacity = a; card.style.transform = `translateY(${(1 - a) * 30}px) scale(${.97 + .03 * a})`;
    rise(q, prog(t, .25, .7) * ex, 14, 6);
    if (q2) rise(q2, prog(t, P.tQ2 ?? 2, .6) * ex, 10, 4);
    yn.style.opacity = prog(t, .7, .5) * ex;
  };
};

// ROLE CARDS (one per audience): P.cards [{role, text, t}]
SCENES.roles = (root, P) => {
  const kick = el('div', { class: 'abs kicker', style: { left: 0, width: '1080px', textAlign: 'center', top: '138px', fontSize: '23px' } }, root, P.kicker || 'Para fazer esta semana');
  const cards = P.cards.map((c, i) => {
    const y = 185 + i * 128;
    const b = panelBox(root, 90, y, 900, 114, { borderRadius: '20px' });
    el('div', { class: 'abs', style: { left: '32px', top: '0', bottom: '0', display: 'flex', alignItems: 'center', width: '150px', font: "italic 400 40px 'Fraunces'", color: PAL.goldL } }, b, c.role);
    el('div', { class: 'abs', style: { left: '190px', right: '28px', top: '10px', bottom: '10px', display: 'flex', alignItems: 'center', font: "600 28px 'Inter Tight'", color: '#fff', lineHeight: 1.2 } }, b, c.text);
    return { b, c };
  });
  return t => {
    const ex = exitK(t, P);
    rise(kick, prog(t, 0, .5) * ex, 12, 4);
    cards.forEach(({ b, c }) => { const k = prog(t, c.t, .6, E.outQuart) * ex; b.style.opacity = k; b.style.transform = `translateX(${(1 - k) * 40}px)`; });
  };
};

// TOOL UI CARD (AI tool for leaders): P.title, P.items [{text,t}]
SCENES.tool = (root, P) => {
  const card = panelBox(root, 110, P.top ?? 150, 860, P.h ?? (100 + P.items.length * 66));
  const bar = el('div', { class: 'abs', style: { left: 0, right: 0, top: 0, height: '62px', borderBottom: '1px solid rgba(201,165,95,.3)', display: 'flex', alignItems: 'center', gap: '10px', padding: '0 26px', boxSizing: 'border-box' } }, card);
  ['#C8644B', PAL.gold, PAL.tealL].forEach(c => el('div', { style: { width: '12px', height: '12px', borderRadius: '50%', background: c, opacity: .8 } }, bar));
  el('div', { style: { marginLeft: '14px', font: "600 22px 'Inter Tight'", color: 'rgba(245,240,230,.85)', letterSpacing: '.06em' } }, bar, P.title || 'Ferramenta do líder · com IA');
  const items = P.items.map((it, i) => {
    const r = el('div', { class: 'abs', style: { left: '34px', right: '34px', top: (90 + i * 68) + 'px', height: '54px', borderRadius: '12px', background: 'rgba(245,240,230,.06)', border: '1px solid rgba(245,240,230,.12)', display: 'flex', alignItems: 'center', gap: '16px', padding: '0 20px', boxSizing: 'border-box', font: "600 27px 'Inter Tight'", color: '#fff' } }, card);
    el('div', { style: { width: '10px', height: '10px', borderRadius: '50%', background: PAL.goldL } }, r);
    el('span', {}, r, it.text);
    return { r, it };
  });
  return t => {
    const ex = exitK(t, P);
    const a = prog(t, 0, .6, E.outQuart) * ex; card.style.opacity = a; card.style.transform = `translateY(${(1 - a) * 30}px)`;
    items.forEach(({ r, it }) => { const k = prog(t, it.t, .45) * ex; r.style.opacity = k; r.style.transform = `translateX(${(1 - k) * 24}px)`; });
  };
};

// CTA FLOW: P.title, P.steps [{text, sub, t}], P.badge {text,t}, P.tArrow, P.arrowText
SCENES.cta = (root, P) => {
  const kick = el('div', { class: 'abs kicker', style: { left: 0, width: '1080px', textAlign: 'center', top: '132px', fontSize: '23px' } }, root, P.kicker || 'Experiência Cultura em Ação');
  const steps = P.steps.map((s, i) => {
    const y = 180 + i * 112;
    const r = el('div', { class: 'abs', style: { left: '120px', width: '840px', top: y + 'px', display: 'flex', gap: '26px', alignItems: 'center' } }, root);
    el('div', { style: { width: '74px', height: '74px', flex: '0 0 auto', borderRadius: '50%', border: `2px solid ${PAL.gold}`, display: 'flex', alignItems: 'center', justifyContent: 'center', font: "italic 400 36px 'Fraunces'", color: PAL.goldL, background: 'rgba(20,35,54,.6)' } }, r, String(i + 1));
    const tx = el('div', { class: 'shadow' }, r);
    el('div', { style: { font: "650 38px 'Inter Tight'", color: '#fff' } }, tx, s.text);
    if (s.sub) el('div', { style: { font: "500 25px 'Inter Tight'", color: 'rgba(245,240,230,.8)', marginTop: '4px' } }, tx, s.sub);
    return { r, s };
  });
  const badge = P.badge ? el('div', { class: 'abs', style: { left: '50%', top: (180 + P.steps.length * 112 + 4) + 'px', transform: 'translateX(-50%)', padding: '12px 30px', borderRadius: '999px', background: PAL.gold, color: '#142336', font: "700 28px 'Inter Tight'", letterSpacing: '.04em', whiteSpace: 'nowrap', boxShadow: '0 10px 30px rgba(0,0,0,.4)', opacity: 0 } }, root, P.badge.text) : null;
  return t => {
    const ex = exitK(t, P);
    rise(kick, prog(t, 0, .5) * ex, 12, 4);
    steps.forEach(({ r, s }) => { const k = prog(t, s.t, .55) * ex; r.style.opacity = k; r.style.transform = `translateX(${(1 - k) * -30}px)`; });
    if (badge) { const k = prog(t, P.badge.t, .5) * ex; badge.style.opacity = k; badge.style.transform = `translateX(-50%) scale(${.9 + .1 * E.outBack(clamp((t - P.badge.t) / .5), 1.3)})`; }
  };
};

// DOWN ARROW "clique no link aqui embaixo" (near the bottom of the frame). P.text
SCENES.linkDown = (root, P) => {
  const box = el('div', { class: 'abs', style: { left: 0, width: '1080px', top: (P.top ?? 1380) + 'px', textAlign: 'center' } }, root);
  const pill = el('div', { style: { display: 'inline-block', padding: '16px 36px', borderRadius: '999px', background: PAL.gold, color: '#142336', font: "700 32px 'Inter Tight'", boxShadow: '0 12px 30px rgba(0,0,0,.45)' } }, box, P.text || 'Inscreva-se no link abaixo');
  const arr = el('div', { style: { font: "400 60px 'Inter Tight'", color: PAL.goldL, marginTop: '6px', textShadow: '0 2px 10px rgba(0,0,0,.5)' } }, box, '↓');
  return t => {
    const ex = exitK(t, P);
    const k = prog(t, 0, .5, E.outQuart) * ex; pill.style.opacity = k; pill.style.transform = `scale(${.9 + .1 * k})`;
    arr.style.opacity = prog(t, .3, .4) * ex; arr.style.transform = `translateY(${Math.sin(t * 5) * 8}px)`;
  };
};

// ELEVATOR MINI callback (top-right badge with floor indicator): P.mode 'up'|'stay', P.text, P.count (optional counter e.g. 15)
SCENES.elevMini = (root, P) => {
  const box = el('div', { class: 'abs', style: { left: (P.left ?? 330) + 'px', width: '420px', top: (P.top ?? 160) + 'px', textAlign: 'center' } }, root);
  const ind = el('div', { style: { margin: '0 auto', width: '190px', height: '82px', borderRadius: '14px', background: 'rgba(10,18,28,.85)', border: '2px solid rgba(201,165,95,.7)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px', font: "700 50px 'Inter Tight'", color: PAL.goldL, fontVariantNumeric: 'tabular-nums', boxShadow: '0 12px 30px rgba(0,0,0,.45)' } }, box);
  const ar = el('span', { style: { fontSize: '34px' } }, ind, P.mode === 'down' ? '▼' : '▲');
  const num = el('span', {}, ind, 'T');
  const box2 = el('div', { style: { position: 'relative', marginTop: '22px', minHeight: '130px' } }, box);
  const texts = P.texts || [{ t: P.tText ?? .5, text: P.text || '' }];
  const txs = texts.map(x => el('div', { class: 'serif shadow', style: { position: 'absolute', left: '-240px', right: '-240px', top: 0, fontSize: (P.size || 50) + 'px', fontStyle: 'italic', color: '#fff', lineHeight: 1.15, opacity: 0 } }, box2, x.text));
  const floors = P.floors || ['T', '1', '2', '3', '4'];
  return t => {
    const ex = exitK(t, P);
    const a = prog(t, 0, .5) * ex; box.style.opacity = a; box.style.transform = `translateY(${(1 - a) * 20}px)`;
    if (P.count != null) {
      const k = prog(t, P.tCount ?? .4, P.countDur ?? 2.2, E.outCubic); num.textContent = String(Math.round(k * P.count)); ar.textContent = '↻';
    } else if (P.mode === 'stay') { num.textContent = 'T'; ar.style.opacity = .3; }
    else { const k = prog(t, P.tMove ?? .4, P.moveDur ?? 1.8, E.inOutCubic); const idx = Math.min(floors.length - 1, Math.floor(k * floors.length)); num.textContent = floors[idx]; ar.style.opacity = .5 + .5 * Math.abs(Math.sin(t * 6)); }
    txs.forEach((e, k) => {
      const tin = texts[k].t, tnext = k + 1 < texts.length ? texts[k + 1].t : 1e9;
      const a2 = prog(t, tin, .55) * (1 - prog(t, tnext - .1, .35)) * ex;
      rise(e, a2, 12, 5);
    });
  };
};
