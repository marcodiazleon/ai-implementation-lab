// C258 (R45): the worked-result table rendered in the browser equals the CLI output, in both languages and widths.
// Usage: node tour_result.js BASE CLI_JSON_FILE
const { chromium } = require("playwright");
const fs = require("fs");
const [base, cliFile] = process.argv.slice(2);
const cli = JSON.parse(fs.readFileSync(cliFile, "utf8"));
(async () => {
  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
  const out = {};
  for (const width of [375, 1360]) for (const lang of ["es", "en"]) {
    const ctx = await browser.newContext({ viewport: { width, height: width > 500 ? 900 : 760 } });
    const p = await ctx.newPage();
    await p.goto(base + "#method"); await p.waitForTimeout(400);
    await p.selectOption("#language", lang); await p.waitForTimeout(250);
    const rows = await p.$$eval("#tourResult tr", (trs) => trs.map((tr) => [...tr.children].map((td) => td.textContent.trim())));
    const intro = await p.$eval(".tour > .muted", (e) => e.textContent);
    const same = rows.length === cli.steps.length && rows.every((r, i) => Number(r[0]) === cli.steps[i].step
      && r[2] === cli.steps[i].result + (cli.steps[i].receipt_id ? " · " + cli.steps[i].receipt_id : "") && Number(r[3]) === cli.steps[i].receipts);
    out[`${lang}@${width}`] = { rows: rows.length, equalsCli: same, installationOutside: /not part of the three minutes|no forma parte de los tres minutos/.test(intro), firstRow: rows[0], lastRow: rows[5] };
    await ctx.close();
  }
  await browser.close();
  console.log(JSON.stringify(out, null, 1));
})();
