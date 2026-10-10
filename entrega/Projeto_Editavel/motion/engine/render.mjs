// Usage: node engine/render.mjs jobs.json [onlyId]
// jobs: [{id, scene, params, duration, fps}] -> out/<id>/%05d.png (RGBA)
import { chromium } from 'playwright-core';
import fs from 'fs'; import path from 'path';
const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const only = process.argv[3] ? process.argv[3].split(',') : null;
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', args: ['--font-render-hinting=none', '--disable-gpu', '--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on('console', m => console.log('[page]', m.text())); page.on('pageerror', e => { console.error('[pageerror]', e.message); process.exitCode = 1; });
const cdp = await page.context().newCDPSession(page);
await cdp.send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } });
await page.goto('file://' + path.resolve('engine/stage.html'));
await page.evaluate(() => document.fonts.ready);
for (const job of jobs) {
  if (only && !only.includes(job.id)) continue;
  const fps = job.fps || 30, n = Math.round(job.duration * fps);
  const dir = path.resolve('out', job.id); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  await page.evaluate(([s, p]) => window.setup(s, p), [job.scene, job.params]);
  await page.evaluate(() => document.fonts.ready);
  const t0 = Date.now();
  const frames = job.preview ? job.preview.map(t => Math.round(t * fps)) : [...Array(n).keys()];
  for (const i of frames) {
    await page.evaluate(t => window.renderAt(t), i / fps);
    const r = await cdp.send('Page.captureScreenshot', { format: 'png', optimizeForSpeed: true });
    fs.writeFileSync(path.join(dir, String(i).padStart(5, '0') + '.png'), Buffer.from(r.data, 'base64'));
  }
  console.log(job.id, frames.length, 'frames', ((Date.now() - t0) / frames.length).toFixed(0), 'ms/frame');
}
await browser.close();
