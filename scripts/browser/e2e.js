// End-to-end checks of U20 behaviors on the public build (and the local server for form language).
// Usage: node e2e.js PUBLIC_BASE LOCAL_BASE OUT_DIR
const { chromium } = require("playwright");
const fs = require("fs");
const [PUBLIC, LOCAL, outDir] = process.argv.slice(2);
fs.mkdirSync(outDir, { recursive: true });
const result = { state: {}, dialog: {}, forms: {}, evidenceError: {}, motion: {}, reflow: {}, errors: [] };

(async () => {
  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
  const page = async (opts = {}) => { const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, ...opts }); const p = await ctx.newPage(); p.on("pageerror", (e) => result.errors.push(e.message)); return [ctx, p]; };

  // C230: draft, provider, model and R11 survive language changes and navigation.
  {
    const [ctx, p] = await page();
    await p.goto(PUBLIC + "#session"); await p.waitForTimeout(500);
    await p.fill("#question", "Borrador U20");
    await p.selectOption("#sessionProvider", "anthropic"); await p.waitForTimeout(300);
    const models = await p.$$eval("#sessionModel option", (os) => os.map((o) => o.value).filter(Boolean));
    await p.selectOption("#sessionModel", models[1] || models[0]);
    const chosen = await p.inputValue("#sessionModel");
    await p.click('a[href="#evidence"]'); await p.waitForSelector("#statusRecords:not([hidden])");
    await p.selectOption("#reqPicker", "R11"); await p.waitForTimeout(200);
    for (const lang of ["en", "es"]) { await p.selectOption("#language", lang); await p.waitForTimeout(250); }
    for (const hash of ["#agents", "#mcp", "#method", "#evidence", "#session"]) { await p.goto(PUBLIC + hash); await p.waitForTimeout(250); }
    result.state = { draft: await p.inputValue("#question"), provider: await p.inputValue("#sessionProvider"), model: await p.inputValue("#sessionModel"), chosen,
      hashAfterEvidence: await p.evaluate(() => location.hash) };
    await p.goto(PUBLIC + "#evidence"); await p.waitForSelector("#statusRecords:not([hidden])");
    result.state.pickerAfterReturn = await p.inputValue("#reqPicker");
    await ctx.close();
  }

  // C229: dialog focus, Escape, focus restore; reduced motion; 320 px reflow.
  {
    const [ctx, p] = await page({ reducedMotion: "reduce" });
    await p.goto(PUBLIC + "#session"); await p.waitForTimeout(500);
    result.motion = { cursorDisplay: await p.$eval(".typing-cursor", (e) => getComputedStyle(e).display), sidebarTransition: await p.$eval(".sidebar", (e) => getComputedStyle(e).transitionDuration) };
    await p.click("#openConnection"); await p.waitForTimeout(200);
    result.dialog.focusInside = await p.evaluate(() => document.getElementById("connectionDialog").contains(document.activeElement));
    result.dialog.firstFocus = await p.evaluate(() => document.activeElement.className || document.activeElement.id);
    const tabs = []; for (let i = 0; i < 6; i++) { await p.keyboard.press("Tab"); tabs.push(await p.evaluate(() => (document.activeElement.id || document.activeElement.tagName) + ":" + document.getElementById("connectionDialog").contains(document.activeElement))); }
    result.dialog.tabStaysInside = tabs;
    await p.keyboard.press("Escape"); await p.waitForTimeout(150);
    result.dialog.afterEscape = await p.evaluate(() => ({ open: document.getElementById("connectionDialog").open, focus: document.activeElement.id }));
    await ctx.close();
    const [ctx2, p2] = await page({ viewport: { width: 320, height: 640 } });
    for (const hash of ["#session", "#agents", "#mcp", "#method", "#evidence/R11"]) { await p2.goto(PUBLIC + hash); await p2.waitForTimeout(400); result.reflow[hash] = await p2.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth); }
    await p2.screenshot({ path: `${outDir}/reflow-320-evidence.jpg`, type: "jpeg", quality: 60 });
    await ctx2.close();
  }

  // C231: native validation messages follow the page language (local server, connection and agent forms).
  {
    const [ctx, p] = await page({ viewport: { width: 1360, height: 900 } });
    await p.goto(LOCAL + "#session"); await p.waitForTimeout(500);
    for (const lang of ["es", "en"]) {
      await p.selectOption("#language", lang); await p.waitForTimeout(200);
      await p.click("#openConnection"); await p.waitForTimeout(200);
      await p.fill("#apiKey", "short"); await p.fill("#apiModel", "");
      await p.click("#connectApi"); await p.waitForTimeout(200);
      const key = await p.$eval("#apiKey", (e) => e.validationMessage), model = await p.$eval("#apiModel", (e) => e.validationMessage);
      await p.keyboard.press("Escape"); await p.waitForTimeout(100);
      await p.goto(LOCAL + "#agents"); await p.waitForTimeout(300);
      await p.fill("#builderName", ""); await p.click("#saveAgent"); await p.waitForTimeout(200);
      const agent = await p.$eval("#builderName", (e) => e.validationMessage);
      result.forms[lang] = { key, model, agent };
      await p.goto(LOCAL + "#session"); await p.waitForTimeout(300);
    }
    await ctx.close();
  }

  // C238 / C261: evidence payload blocked, corrupt JSON, valid JSON of invalid shape, then restored; retry recovers.
  {
    const [ctx, p] = await page({ viewport: { width: 1360, height: 900 } });
    let mode = "blocked";
    // Valid JSON with an invalid shape: the committed payload with an empty run summary and passed kept true (C261).
    const badShape = JSON.stringify(Object.assign(await (await fetch(PUBLIC + "data/latest.json")).json(), { tests: {}, passed: true }));
    await p.route("**/data/latest.json", (route) => mode === "blocked" ? route.abort() : mode === "corrupt" ? route.fulfill({ status: 200, contentType: "application/json", body: "{not json" })
      : mode === "badshape" ? route.fulfill({ status: 200, contentType: "application/json", body: badShape }) : route.continue());
    await p.goto(PUBLIC + "#evidence"); await p.waitForTimeout(800);
    const snap = async () => ({ status: await p.textContent("#evidenceStatus"), retry: await p.$eval("#evidenceRetry", (b) => ({ hidden: b.hidden, name: b.textContent.trim() })), records: await p.$eval("#statusRecords", (e) => e.hidden), explorer: await p.$eval("#evidenceExplorer", (e) => e.hidden) });
    result.evidenceError.blocked = await snap();
    await p.selectOption("#language", "en"); await p.waitForTimeout(200); result.evidenceError.blockedEn = await snap(); await p.selectOption("#language", "es"); await p.waitForTimeout(200);
    mode = "corrupt"; await p.click("#evidenceRetry"); await p.waitForTimeout(600); result.evidenceError.corrupt = await snap();
    mode = "badshape"; await p.click("#evidenceRetry"); await p.waitForTimeout(600);
    result.evidenceError.badShape = Object.assign(await snap(), { evResult: await p.$eval("#evResult", (e) => e.textContent), metricsHidden: await p.$eval("#evidenceMetrics", (e) => e.hidden), live: await p.$eval("#evidenceStatus", (e) => e.getAttribute("role")) });
    await p.selectOption("#language", "en"); await p.waitForTimeout(200); result.evidenceError.badShapeEn = await snap(); await p.selectOption("#language", "es"); await p.waitForTimeout(200);
    mode = "ok"; await p.click("#evidenceRetry"); await p.waitForTimeout(800); result.evidenceError.restored = await snap();
    result.evidenceError.focusAfterRetry = await p.evaluate(() => document.activeElement.id);
    await p.screenshot({ path: `${outDir}/evidence-restored.jpg`, type: "jpeg", quality: 60 });
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync(`${outDir}/e2e.json`, JSON.stringify(result, null, 1));
  console.log(JSON.stringify(result, null, 1));
})();
