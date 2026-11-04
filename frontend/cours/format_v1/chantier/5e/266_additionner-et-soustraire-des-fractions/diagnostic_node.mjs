// Inspection momentanée du seul contrôleur local, sans changement de fichiers.
const r=await fetch('http://127.0.0.1:9229/json/list');
const targets=await r.json();
const ws=new WebSocket(targets[0].webSocketDebuggerUrl);
let seq=0;const pending=new Map();const scripts=new Map();
const request=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});
await new Promise(resolve=>ws.addEventListener('open',resolve,{once:true}));
const done=new Promise(resolve=>{
 ws.addEventListener('message',async e=>{
  const msg=JSON.parse(e.data);
  if(msg.id){const p=pending.get(msg.id);if(p){pending.delete(msg.id);p.resolve(msg.result);}}
  if(msg.method==='Debugger.scriptParsed')scripts.set(msg.params.scriptId,msg.params.url);
  if(msg.method==='Debugger.paused'){
   console.log(msg.params.callFrames.slice(0,10).map(f=>({function:f.functionName,url:scripts.get(f.location.scriptId),line:f.location.lineNumber+1})));
   console.log(JSON.stringify(msg.params.asyncStackTrace));
   const frame=msg.params.callFrames.find(f=>f.functionName==='_rimraf');
   if(frame){console.log(await request('Debugger.evaluateOnCallFrame',{callFrameId:frame.callFrameId,expression:'options.maxRetries=0; options.retryDelay=0; JSON.stringify({path,options})',returnByValue:true}));}
   await request('Debugger.resume');resolve();
  }
 });
});
await request('Debugger.enable');await request('Debugger.setBreakpointByUrl',{url:'node:internal/fs/rimraf',lineNumber:66});await done;ws.close();
