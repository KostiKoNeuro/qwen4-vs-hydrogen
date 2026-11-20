(() => {
 const root=document.documentElement, url=new URL(location.href);
 let saved;try{saved=localStorage.getItem('kk-lang')}catch{}
 const explicit=url.searchParams.get('lang')||url.hash.slice(1);
 const lang=['ru','en'].includes(explicit)?explicit:(saved==='en'?'en':'ru');
 function apply(l,change){
  root.lang=l;root.classList.toggle('ru',l==='ru');
  const title=root.getAttribute('data-title-'+l);if(title)document.title=title;
  for(const b of document.querySelectorAll('[data-set-lang]'))b.setAttribute('aria-pressed',String(b.dataset.setLang===l));
  for(const a of document.querySelectorAll('a[data-local]')){const dest=new URL(a.href);dest.searchParams.set('lang',l);a.href=dest.href;}
  if(change){const u=new URL(location.href);u.searchParams.set('lang',l);if(['#ru','#en'].includes(u.hash))u.hash='';history.replaceState(null,'',u)}
  if(change||['ru','en'].includes(explicit)){try{localStorage.setItem('kk-lang',l)}catch{}}
 }
 apply(lang,false);document.addEventListener('DOMContentLoaded',()=>{apply(lang,false);for(const b of document.querySelectorAll('[data-set-lang]'))b.addEventListener('click',()=>apply(b.dataset.setLang,true));});
})();
