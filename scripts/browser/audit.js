// Responsive and accessibility audit of the public build. Usage: node audit.js BASE_URL OUT_DIR LABEL
const { chromium } = require("playwright");
const fs = require("fs");
const [base, outDir, label] = process.argv.slice(2);
const WIDTHS = [320, 375, 390, 768, 1360];
const VIEWS = [["session", "#session"], ["agents", "#agents"], ["mcp", "#mcp"], ["method", "#method"], ["evidence", "#evidence/R11"]];
fs.mkdirSync(outDir, { recursive: true });

const MEASURE = () => {
  const vis = (e) => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== "hidden" && s.display !== "none"; };
  const inProse = (e) => e.tagName === "A" && ["P", "LI", "TD", "SPAN", "SMALL", "DD", "B"].includes(e.parentElement.tagName);
  const name = (e) => (e.getAttribute("aria-label") || e.labels?.[0]?.textContent || e.textContent || e.getAttribute("placeholder") || "").trim().slice(0, 40);
  const items = [...document.querySelectorAll("a[href],button,select,input:not([type=hidden]),textarea,summary,[tabindex='0']")]
    .filter((e) => vis(e) && !e.closest("[hidden]") && !e.closest("dialog:not([open])"));
  const controls = items.map((e) => { const box = e.type === "checkbox" && e.closest("label") ? e.closest("label") : e; const r = box.getBoundingClientRect(); return { tag: e.tagName.toLowerCase(), id: e.id || null, name: name(e), w: Math.round(r.width), h: Math.round(r.height), prose: inProse(e), accessibleName: !!name(e), viaLabel: box !== e }; });
  const small = controls.filter((c) => !c.prose && (c.w < 44 || c.h < 44));
  const intro = document.querySelector(".presentation"); const composer = document.querySelector("#question");
  return {
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    controls: controls.length, small, unnamed: controls.filter((c) => !c.accessibleName),
    introBottom: intro && !intro.closest("[hidden]") ? Math.round(intro.getBoundingClientRect().bottom) : null,
    composerTop: composer && !composer.closest("[hidden]") ? Math.round(composer.getBoundingClientRect().top) : null,
    viewport: innerHeight,
    h1: [...document.querySelectorAll("h1")].filter(vis).length,
  };
};

(async () => {
  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
  const report = { label, base, pages: [], keyboard: {}, errors: [], consoleErrors: [] };
  for (const lang of ["es", "en"]) for (const width of WIDTHS) {
    const ctx = await browser.newContext({ viewport: { width, height: width >= 768 ? 900 : 760 }, reducedMotion: "reduce" });
    const p = await ctx.newPage();
    p.on("pageerror", (e) => report.errors.push(`${lang}/${width}: ${e.message}`));
    p.on("console", (m) => { if (m.type() === "error") report.consoleErrors.push(`${lang}/${width}: ${m.text().slice(0, 120)}`); });
    await p.goto(base + "#session"); await p.waitForTimeout(500);
    await p.selectOption("#language", lang); await p.waitForTimeout(250);
    for (const [view, hash] of VIEWS) {
      await p.goto(base + hash); await p.waitForTimeout(400);
      if (view === "evidence") await p.waitForSelector("#statusRecords:not([hidden])", { timeout: 5000 }).catch(() => {});
      const m = await p.evaluate(MEASURE);
      report.pages.push({ lang, width, view, ...m });
      if (width !== 768) await p.screenshot({ path: `${outDir}/${label}-${view}-${lang}-${width}.jpg`, type: "jpeg", quality: 60 });
    }
    // Connection dialog: open, measure, Escape, focus restored to the opener.
    await p.goto(base + "#session"); await p.waitForTimeout(300);
    await p.click("#openConnection"); await p.waitForTimeout(200);
    const dialogOpen = await p.evaluate(() => document.getElementById("connectionDialog").open);
    const dm = await p.evaluate(MEASURE);
    report.pages.push({ lang, width, view: "connection-dialog", ...dm, dialogOpen });
    if (width === 375 || width === 1360) await p.screenshot({ path: `${outDir}/${label}-dialog-${lang}-${width}.jpg`, type: "jpeg", quality: 60 });
    await p.keyboard.press("Escape"); await p.waitForTimeout(150);
    const afterEsc = await p.evaluate(() => ({ open: document.getElementById("connectionDialog").open, focus: document.activeElement.id || document.activeElement.tagName }));
    report.keyboard[`${lang}/${width}/dialog`] = { dialogOpen, afterEsc };
    // Expanded rail on small screens: toggle, measure nav links, close with backdrop.
    if (width <= 800) {
      await p.click("#toggleSidebar"); await p.waitForTimeout(200);
      const nav = await p.$$eval("#mainNav a", (as) => as.map((a) => { const r = a.getBoundingClientRect(); return { name: a.getAttribute("aria-label"), w: Math.round(r.width), h: Math.round(r.height) }; }));
      const ov = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      report.keyboard[`${lang}/${width}/rail-expanded`] = { nav, overflow: ov };
      await p.click("#toggleSidebar"); await p.waitForTimeout(150);
    }
    await ctx.close();
  }
  // Keyboard order at 375 and 1360: first 12 Tab stops from the top, plus the skip link target.
  for (const width of [375, 1360]) {
    const ctx = await browser.newContext({ viewport: { width, height: 760 } });
    const p = await ctx.newPage(); await p.goto(base + "#session"); await p.waitForTimeout(400);
    const stops = [];
    for (let i = 0; i < 12; i++) { await p.keyboard.press("Tab"); stops.push(await p.evaluate(() => { const e = document.activeElement; const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return (e.id || e.tagName.toLowerCase()) + (s.outlineStyle !== "none" && s.outlineWidth !== "0px" ? "" : " (no outline)") + (r.width ? "" : " (invisible)"); })); }
    const p2 = await ctx.newPage(); await p2.goto(base + "#session"); await p2.waitForTimeout(400); await p2.keyboard.press("Tab"); await p2.keyboard.press("Enter"); await p2.waitForTimeout(200);
    const skipTarget = await p2.evaluate(() => document.activeElement.id);
    report.keyboard[`${width}/tab-order`] = { stops, skipTarget };
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync(`${outDir}/${label}-audit.json`, JSON.stringify(report, null, 1));
  const worst = report.pages.filter((x) => x.small.length).map((x) => `${x.lang}/${x.width}/${x.view}: ${x.small.length} small (${x.small.slice(0, 4).map((c) => `${c.id || c.tag} ${c.w}x${c.h}`).join(", ")})`);
  console.log(JSON.stringify({ errors: report.errors, consoleErrors: [...new Set(report.consoleErrors)].slice(0, 5), maxOverflow: Math.max(...report.pages.map((x) => x.overflow)), small: worst.length, sample: worst.slice(0, 8), intro375: report.pages.find((x) => x.width === 375 && x.view === "session" && x.lang === "es") }, null, 1));
})();
