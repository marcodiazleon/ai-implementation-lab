// C278 (R54d) and C289 (R55e): browser checks of the security boundaries, run under scripts/sandbox/run_isolated.sh.
// Usage: node security.js LOCAL_BASE PUBLIC_BASE
//   LOCAL_BASE  a local server started with a fake provider (see scripts/browser/security_server.py)
//   PUBLIC_BASE a static server over the public build (_site) with the CSP meta element
// Prints JSON; every value is observed, nothing is asserted here (the report and the acceptance records read it).
const { chromium } = require("playwright");
const [local, pub] = process.argv.slice(2);
const DUMMY = "sk-" + "proj-" + "u".repeat(40); // non-functional, assembled at runtime
(async () => {
  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
  const out = { secrets: {}, csp: {} };
  // C278: dummy key through the dialog; the page must not keep it and must render provider text literally.
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const consoleErrors = [];
  page.on("console", (m) => { if (m.type() === "error") consoleErrors.push(m.text()); });
  await page.goto(local + "/#session"); await page.waitForTimeout(500);
  await page.click("#openConnection"); await page.waitForTimeout(200);
  await page.fill("#apiKey", DUMMY); await page.check("#apiConsent");
  await page.click("#connectApi"); await page.waitForTimeout(800);
  out.secrets.keyFieldAfterSubmit = await page.$eval("#apiKey", (e) => e.value);
  out.secrets.connectionStatus = await page.$eval("#connectionStatus", (e) => e.textContent);
  await page.keyboard.press("Escape"); await page.waitForTimeout(200);
  await page.fill("#question", "render this"); await page.click("#sendQuestion"); await page.waitForTimeout(800);
  const html = await page.$eval("#messages", (e) => e.innerHTML);
  out.secrets.messageContainsImgElement = /<img/i.test(html);
  out.secrets.messageShowsMarkupAsText = await page.$eval("#messages", (e) => e.textContent.includes("<img src=x onerror=alert(1)>"));
  out.secrets.messageText = await page.$eval("#messages article:last-child p", (e) => e.textContent);
  await page.fill("#question", "fail now"); await page.click("#sendQuestion"); await page.waitForTimeout(800);
  out.secrets.chatNoticeAfterError = await page.$eval("#chatNotice", (e) => e.textContent);
  const storage = await page.evaluate(() => Object.fromEntries(Object.keys(localStorage).map((k) => [k, localStorage.getItem(k)])));
  out.secrets.localStorageKeys = Object.keys(storage);
  out.secrets.dummyInLocalStorage = JSON.stringify(storage).includes(DUMMY);
  out.secrets.dummyInDocument = (await page.content()).includes(DUMMY);
  out.secrets.dummyInConsoleErrors = consoleErrors.some((t) => t.includes(DUMMY));
  out.secrets.dummyInChatNotice = out.secrets.chatNoticeAfterError.includes(DUMMY);
  await ctx.close();
  // C289: the public build with the CSP meta element loads every view without a CSP violation.
  for (const [name, base] of [["public", pub], ["local", local]]) {
    const c = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const p = await c.newPage();
    const violations = [];
    p.on("console", (m) => { if (/Content Security Policy|Refused to/i.test(m.text())) violations.push(m.text()); });
    const views = {};
    for (const view of ["session", "agents", "mcp", "method", "evidence"]) {
      await p.goto(base + "/#" + view); await p.waitForTimeout(600);
      views[view] = await p.$eval("#view-" + (view === "session" ? "demo" : view), (e) => !e.hidden && e.textContent.trim().length > 0);
    }
    const meta = await p.$eval("meta[http-equiv='Content-Security-Policy']", (e) => e.content).catch(() => null);
    const agentCard = await p.$eval("#templateCards", (e) => e.children.length).catch(() => -1);
    out.csp[name] = { metaCsp: meta, viewsRendered: views, templateCards: agentCard, violations };
    await c.close();
  }
  await browser.close();
  console.log(JSON.stringify(out, null, 1));
})();
