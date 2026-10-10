// Deterministic animation helpers. Every scene is a pure function of time t (seconds).
const E = {
  linear: x => x,
  inCubic: x => x * x * x,
  outCubic: x => 1 - Math.pow(1 - x, 3),
  outQuart: x => 1 - Math.pow(1 - x, 4),
  outQuint: x => 1 - Math.pow(1 - x, 5),
  inOutCubic: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
  inOutQuart: x => x < .5 ? 8 * x * x * x * x : 1 - Math.pow(-2 * x + 2, 4) / 2,
  inOutSine: x => -(Math.cos(Math.PI * x) - 1) / 2,
  outBack: (x, s = 1.2) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2),
};
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
// progress of t inside [t0, t0+d] with easing
const prog = (t, t0, d, ease = E.outCubic) => ease(clamp((t - t0) / d));
const lerp = (a, b, k) => a + (b - a) * k;
// enter/exit envelope: 0 before tin, ramps to 1 over din, holds, ramps to 0 over dout ending at tout
function env(t, tin, tout, din = .6, dout = .45, ein = E.outCubic, eout = E.inOutCubic) {
  if (t < tin || t > tout) return 0;
  const a = ein(clamp((t - tin) / din));
  const b = 1 - eout(clamp((t - (tout - dout)) / dout));
  return Math.min(a, b);
}
const PAL = {
  navy: '#142336', navy2: '#1B2D44', teal: '#2E7282', tealL: '#4A93A3', gold: '#C9A55F', goldL: '#E2C88F',
  cream: '#F5F0E6', white: '#FFFFFF', ink: '#0B1420', red: '#C8644B',
};
function el(tag, attrs = {}, parent = null, html = null) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'style') Object.assign(e.style, v); else if (k === 'class') e.className = v; else e.setAttribute(k, v);
  }
  if (html !== null) e.innerHTML = html;
  if (parent) parent.appendChild(e);
  return e;
}
function svgEl(tag, attrs = {}, parent = null) {
  const e = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  if (parent) parent.appendChild(e);
  return e;
}
// apply a standard "rise + fade + unblur" state for amount a in [0,1]
function rise(e, a, dy = 28, blur = 8, extra = '') {
  e.style.opacity = a;
  e.style.transform = `translateY(${(1 - a) * dy}px) ${extra}`;
  e.style.filter = blur && a < 1 ? `blur(${(1 - a) * blur}px)` : 'none';
}
window.SCENES = {};
