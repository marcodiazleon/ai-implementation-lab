// R53a: payload per view and layout shift, from the browser's own performance entries. No score.
// Usage: node perf.js BASE OUT_FILE
const { chromium } = require("playwright");
const fs = require("fs");
const [base, out] = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
  const report = {};
  for (const [view, hash] of [["session", "#session"], ["method", "#method"], ["evidence", "#evidence/R11"], ["agents", "#agents"], ["mcp", "#mcp"]]) {
    for (const width of [375, 1360]) {
      const ctx = await browser.newContext({ viewport: { width, height: width > 500 ? 900 : 760 } });
      const p = await ctx.newPage();
      await p.addInitScript(() => { window.__cls = 0; new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: "layout-shift", buffered: true }); });
      await p.goto(base + hash, { waitUntil: "networkidle" }); await p.waitForTimeout(800);
      const data = await p.evaluate(() => {
        const nav = performance.getEntriesByType("navigation")[0];
        const res = performance.getEntriesByType("resource").map((r) => ({ name: r.name.split("/").slice(-1)[0], bytes: r.encodedBodySize, decoded: r.decodedBodySize }));
        const total = res.reduce((s, r) => s + r.bytes, 0) + (nav ? nav.encodedBodySize : 0);
        return { html: nav ? nav.encodedBodySize : null, domContentLoaded: nav ? Math.round(nav.domContentLoadedEventEnd) : null, load: nav ? Math.round(nav.loadEventEnd) : null,
          resources: res.length, transferredBytes: total, largest: res.sort((a, b) => b.bytes - a.bytes).slice(0, 5), layoutShift: Number(window.__cls.toFixed(4)) };
      });
      report[`${view}@${width}`] = data;
      await ctx.close();
    }
  }
  await browser.close();
  fs.writeFileSync(out, JSON.stringify(report, null, 1));
  for (const [k, v] of Object.entries(report)) console.log(k, "bytes", v.transferredBytes, "resources", v.resources, "DCL", v.domContentLoaded, "ms", "CLS", v.layoutShift, "largest", v.largest.slice(0, 3).map((r) => r.name + ":" + r.bytes).join(" "));
})();
