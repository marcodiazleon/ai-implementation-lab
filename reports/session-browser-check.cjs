const { chromium } = require(process.env.LAB_PLAYWRIGHT_MODULE || 'playwright');
const { spawn } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const local=process.argv.includes('--local');
const child = spawn('python', local?[path.join(root,'run.py'),'serve','--port','18765']:['-m','http.server','18765','--bind','127.0.0.1','--directory',path.join(root,'_site')], {cwd:root,windowsHide:true,stdio:'ignore'});
(async()=>{
 let browser;
 try {
  browser=await chromium.launch({headless:true});
  const page=await browser.newPage({viewport:{width:1440,height:900}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  let ready=false;for(let i=0;i<30;i++){try{await page.goto('http://127.0.0.1:18765');ready=true;break;}catch{await new Promise(r=>setTimeout(r,100));}}
  if(!ready)throw Error('Static server unavailable');
  await page.locator('#question').fill('Synthetic draft for session review');
  const checks={};
  checks.navigation=[];
  for(const hash of ['agents','mcp','method','evidence','session']){
   await page.goto('http://127.0.0.1:18765/#'+hash);
   const view=hash==='session'?'demo':hash;
   checks.navigation.push({hash,visible:await page.locator('#view-'+view).isVisible()});
  }
  checks.draftPreserved=await page.locator('#question').inputValue()==='Synthetic draft for session review';
  checks.providers={};
  for(const provider of ['anthropic','openai']){
   await page.locator('#sessionProvider').selectOption(provider);
   checks.providers[provider]=await page.locator('#sessionModel').evaluate(n=>[...n.options].map(o=>o.value));
  }
  await page.locator('#language').selectOption('en');
  checks.english=await page.locator('html').getAttribute('lang')==='en';
  checks.englishNavigation=await page.locator('[data-view="demo"]').innerText();
  await page.locator('#language').selectOption('es');
  checks.spanish=await page.locator('html').getAttribute('lang')==='es';
  checks.languagePreservesDraft=await page.locator('#question').inputValue()==='Synthetic draft for session review';
  checks.controls=await page.locator('select').evaluateAll(nodes=>nodes.map(n=>({id:n.id,options:[...n.options].map(o=>o.value)})));
  await page.screenshot({path:path.join(root,'reports/session-'+(local?'local-':'')+'desktop.png'),fullPage:true});
  await page.goto('http://127.0.0.1:18765/#connection');
  checks.dialogOpen=await page.locator('#connectionDialog').evaluate(n=>n.open);
  await page.keyboard.press('Escape');
  checks.dialogEscapeClosed=await page.locator('#connectionDialog').evaluate(n=>!n.open);
  await page.locator('#sessionProvider').focus();await page.keyboard.press('Tab');
  checks.keyboardNext=await page.evaluate(()=>document.activeElement.id);
  checks.publicKeyDisabled=await page.locator('#apiKey').isDisabled();
  await page.setViewportSize({width:390,height:844});
  checks.mobileNoPageOverflow=await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
  await page.locator('#toggleSidebar').click();
  await page.locator('[data-view="agents"]').click();
  await page.locator('#view-agents').waitFor({state:'visible'});
  checks.mobileNavigation=await page.locator('#view-agents').isVisible();
  await page.goto('http://127.0.0.1:18765/#session');
  await page.screenshot({path:path.join(root,'reports/session-'+(local?'local-':'')+'mobile.png'),fullPage:true});
  checks.errors=errors;
  fs.writeFileSync(path.join(root,'reports/session-'+(local?'local-':'')+'browser-check.json'),JSON.stringify({revision:'95c1795',mode:(local?'local backend':'static build')+' synthetic; headless Chromium',checks},null,2));
  console.log(JSON.stringify(checks));
 }finally{if(browser)await browser.close();child.kill();}
})().catch(e=>{console.error(e);process.exitCode=1;});
