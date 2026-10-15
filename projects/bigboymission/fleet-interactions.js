(function(){
  const stylesheet=document.createElement('link');stylesheet.rel='stylesheet';stylesheet.href='/fleet-interactions.css';document.head.appendChild(stylesheet);
  const help={
    working:'A live worker attempt or current heartbeat is present.',
  online:'The orchestrator is reachable through Hermes or AI Share, but no active task evidence is present.',
    blocked:'The profile has open work classified as blocked and needs a decision or recovery.',
    ready:'The profile is configured and has assigned work, but no live run is currently verified.',
    idle:'The profile is configured, with no open assignment or current runtime activity.'
  };
  const keys=['working','online','blocked','ready','idle'];
  function markExternalCards(){
    document.querySelectorAll('[data-agent="miumiu"] .agent-footer span:first-child').forEach(node=>{
      node.className='online-text';
      node.textContent='● AI Share external';
    });
  }
  function enhance(){
    const summary=document.querySelector('#agent-summary'),helpBox=document.querySelector('#agent-status-help'),select=document.querySelector('#agent-status-filter');
    if(!summary||!helpBox||!select||!summary.children.length)return;
    markExternalCards();
    const selected=select.value;
    if(summary.querySelector('[data-agent-status]')){
      const active=summary.querySelector('.selected');
      helpBox.innerHTML=selected==='all'?'<b>Fleet status guide</b><span>Click a status to show only agents in that state. Click it again to return to all agents.</span>':`<b>${selected.toUpperCase()}</b><span>${esc(help[selected])}</span>`;
      return;
    }
    [...summary.children].forEach((node,i)=>{
      const key=keys[i];
      const count=node.querySelector('b')?.textContent||'0';
      node.outerHTML=`<button type="button" class="status-filter ${selected===key?'selected':''}" data-agent-status="${key}" title="${help[key]}" aria-label="Filter agents by ${key}: ${help[key]}">${badge(key)} <b>${esc(count)}</b></button>`;
    });
    helpBox.innerHTML=selected==='all'
      ? '<b>Fleet status guide</b><span>Click a status to show only agents in that state. Click it again to return to all agents.</span>'
      : `<b>${selected.toUpperCase()}</b><span>${esc(help[selected])}</span>`;
    markExternalCards();
  }
  document.addEventListener('click',e=>{
    const button=e.target.closest('[data-agent-status]');
    if(!button)return;
    const select=document.querySelector('#agent-status-filter');
    select.value=select.value===button.dataset.agentStatus?'all':button.dataset.agentStatus;
    select.dispatchEvent(new Event('change'));
  });
  window.setInterval(enhance,250);
  enhance();
})();
