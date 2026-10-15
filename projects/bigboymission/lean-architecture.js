(function(){
  const style=document.createElement('style');style.textContent='.nav{display:flex;align-items:center}.nav span{flex:1;min-width:0}.nav-count{display:inline-flex;align-items:center;justify-content:center;min-width:21px;height:21px;margin-left:10px;padding:0 6px;box-sizing:border-box;background:#eaf2ff;color:#1e6ee8;border:1px solid #c8dcfb;border-radius:999px;font-size:11px;line-height:1}';document.head.appendChild(style);
  const embedStyle=document.createElement('style');embedStyle.textContent='.system-backend-view>#system-backend-root{height:auto}.system-backend-view .archify-reference{height:auto;margin:0;border:0;border-radius:16px;overflow:hidden;background:#f4f7fb}.system-backend-view .archify-reference iframe{border-radius:16px;box-shadow:none;background:#f4f7fb}';document.head.appendChild(embedStyle);
  const duplicateSelectors=['.arch-identity','.arch-share','.arch-connectors','.arch-fleet','.structure-editor'];
  function clean(){
    const root=document.querySelector('#architecture-root');if(!root)return;
    duplicateSelectors.forEach(selector=>root.querySelectorAll(selector).forEach(node=>node.remove()));
  }
  setInterval(clean,250);clean();
})();
