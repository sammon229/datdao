(function(){
  document.title='BigBoyMission';
  const stylesheet=document.createElement('link');stylesheet.rel='stylesheet';stylesheet.href='/resources.css';document.head.appendChild(stylesheet);
  const escText=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const fmtBytes=v=>{const n=Number(v||0);if(!n)return '—';const units=['B','GB','TB'];let x=n,u=0;while(x>=1024*1024*1024&&u<2){x/=1024*1024*1024;u++}return `${x.toFixed(u?1:0)} ${units[u]}`};
  const level=p=>p>=90?'danger':p>=75?'warn':'';
  const bar=(p)=>`<div class="resource-bar"><i class="${level(p)}" style="width:${Math.max(0,Math.min(100,p||0))}%"></i></div>`;
  const state=p=>p>=90?'HIGH':p>=75?'ELEVATED':'HEALTHY';
  function ensure(){
    if(document.querySelector('#resource-panel'))return document.querySelector('#resource-panel');
    const target=document.querySelector('#runtime-cards');if(!target)return null;
    const panel=document.createElement('section');panel.id='resource-panel';panel.className='panel resource-panel';panel.innerHTML='<div class="head"><div><label>HOST RESOURCE PULSE</label><h2>Computer usage</h2></div><span id="resource-captured">Reading live counters…</span></div><div id="resource-grid" class="resource-grid"></div><p id="resource-note" class="resource-note"></p>';
    target.parentNode.insertBefore(panel,target);return panel;
  }
  function render(d){
    const panel=ensure();if(!panel||!d)return;
    const memTotal=Number(d.memoryTotal||0),memFree=Number(d.memoryFree||0),memUsed=Math.max(0,memTotal-memFree),memPct=memTotal?memUsed/memTotal*100:0;
    const disks=(Array.isArray(d.disks)?d.disks:(d.disks?[d.disks]:[])).filter(x=>x.total);const disk=disks[0],diskPct=disk?((disk.total-disk.free)/disk.total*100):0;
    const gpuUsage=Array.isArray(d.gpuUsage)?d.gpuUsage:(d.gpuUsage?[d.gpuUsage]:[]);const gpu=gpuUsage[0],gpuDevices=Array.isArray(d.gpus)?d.gpus:(d.gpus?[d.gpus]:[]);const cpu=Number(d.cpuPercent||0);
    const gpuCard=gpu?`<article class="resource-card"><header><b>GPU</b><span class="resource-state ${level(gpu.utilization)}">${state(gpu.utilization)}</span></header><div class="resource-value">${gpu.utilization.toFixed(0)}%</div><div class="resource-sub">${escText(gpu.name)} · ${gpu.memoryUsed.toFixed(0)} / ${gpu.memoryTotal.toFixed(0)} MB VRAM</div>${bar(gpu.utilization)}</article>`:`<article class="resource-card"><header><b>GPU</b><span class="resource-state">DETECTED</span></header><div class="resource-value">—</div><div class="resource-sub">${escText(gpuDevices.map(x=>x.name).join(', ')||'No GPU adapter reported')} · utilization unavailable</div></article>`;
    document.querySelector('#resource-grid').innerHTML=`<article class="resource-card"><header><b>CPU</b><span class="resource-state ${level(cpu)}">${state(cpu)}</span></header><div class="resource-value">${cpu.toFixed(0)}%</div><div class="resource-sub">Total processor utilization</div>${bar(cpu)}</article><article class="resource-card"><header><b>RAM</b><span class="resource-state ${level(memPct)}">${state(memPct)}</span></header><div class="resource-value">${memPct.toFixed(0)}%</div><div class="resource-sub">${fmtBytes(memUsed)} used of ${fmtBytes(memTotal)} · ${fmtBytes(memFree)} free</div>${bar(memPct)}</article>${gpuCard}<article class="resource-card"><header><b>STORAGE</b><span class="resource-state ${level(diskPct)}">${state(diskPct)}</span></header><div class="resource-value">${disk?diskPct.toFixed(0)+'%':'—'}</div><div class="resource-sub">${disk?escText(disk.name)+' · '+fmtBytes(disk.free)+' free of '+fmtBytes(disk.total):'No fixed disk data reported'}</div>${disk?bar(diskPct):''}</article>`;
    document.querySelector('#resource-captured').textContent=d.capturedAt?`Captured ${new Date(d.capturedAt).toLocaleTimeString([], {hour:'numeric',minute:'2-digit',second:'2-digit'})}`:'Live host counters';
    document.querySelector('#resource-note').textContent='Read-only local telemetry. GPU utilization and VRAM are shown when nvidia-smi is available; otherwise the adapter is identified without usage claims.';
  }
  async function refresh(){if(!document.querySelector('#systems-view.active'))return;try{const r=await fetch('/api/runtime',{cache:'no-store'});const d=await r.json();render(d.resources)}catch(e){const n=document.querySelector('#resource-note');if(n)n.textContent='Resource telemetry temporarily unavailable.'}}
  setInterval(refresh,1500);setInterval(ensure,500);ensure();
})();
