const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1100,height:430},deviceScaleFactor:2});
for(const n of process.argv.slice(2)){await p.goto('file://'+process.cwd()+'/'+n+'.html');await p.waitForTimeout(1500);await p.evaluate(()=>document.fonts.ready);await p.screenshot({path:n+'.png',omitBackground:true});}
await b.close();})();
