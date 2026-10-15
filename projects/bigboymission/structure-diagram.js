(function(){
  const css=document.createElement('link');css.rel='stylesheet';css.href='/reference-embed.css';document.head.appendChild(css);
  function inject(){
    const root=document.querySelector('#architecture-root'),anchor=root?.querySelector('.arch-share');
    if(!root||!anchor||root.querySelector('.archify-reference'))return;
    anchor.insertAdjacentHTML('beforebegin','<section class="archify-reference" aria-label="AI Share Agent Architecture"><iframe title="AI Share Agent Architecture" src="/reference/ai-share-agent-architecture.html?theme=light"></iframe></section>');
    wireSingleScroll();
  }
  function wireSingleScroll(){
    document.querySelectorAll('.archify-reference iframe,.system-backend-frame iframe').forEach(frame=>{
      if(frame.dataset.singleScroll)return;
      frame.dataset.singleScroll='true';
      const fit=()=>{
        try{
          const doc=frame.contentDocument;if(!doc)return;
            if(!doc.getElementById('mission-control-embed-overrides')){
              const style=doc.createElement('style');
              style.id='mission-control-embed-overrides';
              style.textContent='html,body{background:#f4f7fb!important}html[data-preset="blueprint"] body{background-image:none!important;background-attachment:initial!important}@media (min-width:960px){.cards{grid-template-columns:repeat(4,minmax(0,1fr))!important;gap:12px!important}.cards .card{min-width:0;padding:1rem!important}}';
              (doc.head||doc.documentElement).appendChild(style);
            }
          const rootDoc=doc.documentElement;
          const body=doc.body;
          const svg=doc.querySelector('.diagram-container>svg,svg');
          const content=doc.querySelector('.container');
          const cards=doc.querySelector('.cards');
          const outline=doc.querySelector('.node-outline');
          const bottom=(node)=>{const rect=node?.getBoundingClientRect();return rect?rect.bottom:0;};
          const height=Math.max(
            rootDoc?.scrollHeight||0,
            body?.scrollHeight||0,
            rootDoc?.offsetHeight||0,
            body?.offsetHeight||0,
            bottom(svg),
            bottom(content),
            bottom(cards),
            bottom(outline)
          );
          if(height>0)frame.style.height=Math.min(Math.max(Math.ceil(height+24),720),12000)+'px';
          rootDoc.style.overflow='hidden';
          if(body)body.style.overflow='hidden';
        }catch(_){/* keep the safe fixed fallback if the reference is unavailable */}
      };
      frame.addEventListener('load',()=>{fit();setTimeout(fit,250);setTimeout(fit,1000);setTimeout(fit,2000);});
      if(frame.contentDocument?.readyState==='complete')fit();
    });
  }
  function addSystemBackend(){
    if(document.querySelector('#system-backend-view'))return;
    const local=document.querySelector('.local'),footer=document.querySelector('main>footer');
    if(!local||!footer)return;
    local.insertAdjacentHTML('beforebegin','<button class="nav" data-view="system-backend">⌘ <span>System Backend</span></button>');
    footer.insertAdjacentHTML('beforebegin','<section id="system-backend-view" class="view system-backend-view"><div id="system-backend-root"><div class="system-backend-stats"><span><b>17</b> mapped nodes</span><span><b>4</b> storage layers</span><span><b>1</b> canonical task identity</span><span><b>∞</b> execution paths</span></div><section class="archify-reference" aria-label="Mission Control Unified AI Systems Backend"><iframe title="Mission Control Unified AI Systems Backend" src="/reference/mission-control-unified-architecture.html?theme=light"></iframe></section><div class="system-backend-notes"><article><label>CONTROL FLOW</label><strong>Dat → BigBoy → Hermes / MiuMiu</strong><p>Dat remains the final authority. BigBoy coordinates execution and routes engineering overflow through the canonical AI Share task identity.</p></article><article><label>STATE OWNERSHIP</label><strong>AI Share + Kanban + state.db</strong><p>AI Share carries Inbox, Outbox, Status, and Results while Kanban and Hermes databases retain operational evidence.</p></article><article><label>MEMORY & KNOWLEDGE</label><strong>Mnemosyne + Obsidian</strong><p>Mnemosyne stores durable structured memory. Obsidian remains the human-readable knowledge and review surface.</p></article></div></div></section>');
    const style=document.createElement('style');style.textContent='.system-backend-view{height:auto;min-height:0;padding-bottom:20px;overflow:visible}.system-backend-intro{display:flex;justify-content:space-between;gap:18px;align-items:flex-start;margin:0 0 12px}.system-backend-intro label,.system-backend-notes label{color:#2c78df;font-size:10px;letter-spacing:.12em;font-weight:800}.system-backend-intro h2{margin:4px 0;color:#17365d}.system-backend-intro p{margin:0;max-width:760px;color:#637994}.system-backend-intro .state{color:#167b58;font-size:10px;font-weight:800;letter-spacing:.1em;white-space:nowrap}.system-backend-stats{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 14px}.system-backend-stats span{display:inline-flex;align-items:center;gap:7px;padding:8px 11px;border:1px solid #d8e4f2;border-radius:10px;background:#f7fbff;color:#637994;font-size:12px}.system-backend-stats b{color:#1f5fae;font-size:16px}.system-backend-view .archify-reference{height:auto;margin:0;border:0;border-radius:16px;overflow:hidden;background:#f4f7fb}.system-backend-view .archify-reference iframe{display:block;width:100%;height:2340px;min-height:2340px;border:0;border-radius:16px;background:#f4f7fb}.system-backend-notes{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:14px}.system-backend-notes article{padding:15px;border:1px solid #d8e4f2;border-radius:14px;background:#fff;box-shadow:0 8px 24px rgba(27,48,78,.05)}.system-backend-notes strong{display:block;margin:7px 0 5px;color:#17365d}.system-backend-notes p{margin:0;color:#637994;font-size:12px;line-height:1.5}@media(max-width:700px){.system-backend-intro{flex-direction:column}.system-backend-notes{grid-template-columns:1fr}.system-backend-view .archify-reference iframe{height:4200px;min-height:4200px}}';document.head.appendChild(style);wireSingleScroll();
  }
  function activateSystemBackend(){
    document.addEventListener('click',e=>{const nav=e.target.closest('[data-view="system-backend"]');if(!nav)return;e.preventDefault();document.querySelectorAll('.nav').forEach(x=>x.classList.toggle('active',x.dataset.view==='system-backend'));document.querySelectorAll('.view').forEach(x=>x.classList.remove('active'));document.querySelector('#system-backend-view')?.classList.add('active');const title=document.querySelector('#title');if(title)title.textContent='System Backend';document.title='BigBoyMission · System Backend';window.scrollTo({top:0,left:0,behavior:'instant'});});
  }
  setInterval(()=>{inject();addSystemBackend();wireSingleScroll();},250);inject();addSystemBackend();activateSystemBackend();wireSingleScroll();
})();
