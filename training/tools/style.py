"""Stylesheet for the SAP Migration Training Handbook (screen + print-to-PDF)."""

CSS = r"""
:root{
  --navy:#0f2b4c; --navy2:#173a63; --blue:#1b4f86; --sky:#e8f0fb; --skyb:#9ec3ec;
  --ink:#12263f; --body:#334e68; --muted:#5b7288; --faint:#7b8794;
  --line:#dbe3ec; --line2:#e8edf3; --bg:#f5f7fa; --paper:#ffffff;
  --green:#e6f4ea; --greenb:#3d9a5f; --amber:#fdf3d8; --amberb:#d9a520;
  --red:#fdecec; --redb:#c8434b; --grey:#f3f5f9;
  --serif:"Source Serif 4","Source Serif Pro",Georgia,"Times New Roman",serif;
  --sans:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --mono:"SFMono-Regular",Menlo,Consolas,"Liberation Mono",monospace;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--body);font-family:var(--sans);
  font-size:15.5px;line-height:1.62;font-variant-numeric:tabular-nums;}
h1,h2,h3,h4,h5{color:var(--navy);font-weight:800;line-height:1.24;letter-spacing:-.012em;margin:0}
a{color:var(--blue);text-decoration:none}
a:hover{text-decoration:underline}
code,kbd,samp{font-family:var(--mono);font-size:.88em;background:#eef2f7;border:1px solid var(--line);
  border-radius:4px;padding:.08em .34em;color:#123a63}

/* ---------- layout ---------- */
.shell{display:flex;gap:0;max-width:1600px;margin:0 auto;align-items:flex-start}
.rail{position:sticky;top:0;width:296px;flex:0 0 296px;height:100vh;overflow-y:auto;
  background:linear-gradient(180deg,#0f2b4c,#122f54 60%,#0d2440);color:#c9d8ea;padding:26px 20px 40px}
.rail .brand{font-size:12px;letter-spacing:.16em;color:#7fa8d4;font-weight:800;margin-bottom:8px}
.rail .ttl{font-size:17px;font-weight:800;color:#fff;line-height:1.3;margin-bottom:4px}
.rail .subttl{font-size:11.5px;color:#8fabc9;margin-bottom:20px;line-height:1.5}
.rail .prog{height:5px;background:#1d3f68;border-radius:3px;overflow:hidden;margin:0 0 20px}
.rail .prog i{display:block;height:100%;width:0;background:linear-gradient(90deg,#4d90d4,#7fd0a0);transition:width .25s}
.rail .progtxt{font-size:11px;color:#7fa8d4;margin:-14px 0 18px}
.rail nav a{display:flex;gap:9px;align-items:baseline;padding:6px 10px;border-radius:7px;
  color:#b9cde2;font-size:13px;line-height:1.35;margin-bottom:1px}
.rail nav a .n{font-variant-numeric:tabular-nums;color:#6d92b9;font-weight:700;font-size:11.5px;min-width:20px}
.rail nav a:hover{background:#1a3b62;color:#fff;text-decoration:none}
.rail nav a.active{background:#21497a;color:#fff}
.rail nav a.active .n{color:#9fc4ea}
.rail .grp{font-size:10.5px;letter-spacing:.14em;color:#6d92b9;font-weight:800;margin:16px 0 6px 10px}
.rail .railfoot{margin-top:24px;padding-top:16px;border-top:1px solid #1d3f68;font-size:11px;color:#7fa8d4;line-height:1.6}
.paper{flex:1 1 auto;min-width:0;background:var(--paper);box-shadow:0 0 0 1px var(--line),0 18px 50px -30px rgba(15,43,76,.45)}
.wrap{padding:0 clamp(20px,4.2vw,76px) 90px}

/* ---------- top bar (screen) ---------- */
.topbar{position:sticky;top:0;z-index:40;display:flex;align-items:center;gap:14px;
  padding:10px clamp(20px,4.2vw,76px);background:rgba(255,255,255,.94);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--line);font-size:12.5px;color:var(--muted)}
.topbar .dot{width:8px;height:8px;border-radius:50%;background:var(--greenb);box-shadow:0 0 0 3px #d9efe0}
.topbar b{color:var(--navy);font-weight:700}
.topbar .sp{flex:1}
.btn{border:1px solid var(--line);background:#fff;color:var(--navy);border-radius:8px;padding:6px 12px;
  font-size:12.5px;font-weight:700;cursor:pointer;font-family:inherit}
.btn:hover{border-color:var(--skyb);background:var(--sky)}
.btn.primary{background:var(--navy);border-color:var(--navy);color:#fff}
.btn.primary:hover{background:var(--blue)}

/* ---------- cover ---------- */
.cover{position:relative;padding:clamp(34px,5vw,72px) clamp(20px,4.2vw,76px) 44px;
  background:linear-gradient(135deg,#0b1f38 0%,#0f2b4c 45%,#1b4f86 100%);color:#e7eef7;overflow:hidden}
.cover:before{content:"";position:absolute;inset:0;
  background:radial-gradient(760px 420px at 88% -8%,rgba(120,180,240,.28),transparent 62%),
             radial-gradient(620px 380px at 6% 108%,rgba(90,200,160,.16),transparent 60%);}
.cover>*{position:relative}
.cover .eyebrow{font-size:11.5px;letter-spacing:.22em;font-weight:800;color:#8fc0ee;margin-bottom:18px}
.cover h1{color:#fff;font-size:clamp(30px,4.4vw,52px);line-height:1.1;letter-spacing:-.02em;margin-bottom:14px}
.cover .lede{font-size:clamp(14px,1.4vw,17.5px);color:#c3d6ea;max-width:820px;line-height:1.62;margin-bottom:26px}
.cover .tags{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:34px}
.cover .tags span{font-size:11.5px;font-weight:700;letter-spacing:.05em;color:#dce9f7;
  background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.22);padding:5px 11px;border-radius:99px}
.cover .rule{height:1px;background:rgba(255,255,255,.22);margin:0 0 24px}
.docctl{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:1px;
  background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.18);border-radius:12px;overflow:hidden}
.docctl div{background:rgba(10,26,47,.62);padding:12px 15px}
.docctl dt{font-size:10.5px;letter-spacing:.13em;color:#8fc0ee;font-weight:800;margin-bottom:4px}
.docctl dd{margin:0;font-size:13.5px;color:#eaf1f9;font-weight:600;line-height:1.45}
.cover .stamp{margin-top:22px;font-size:11.5px;color:#9db8d4;line-height:1.6}

/* ---------- running header / footer (print) ---------- */
.rhead,.rfoot{display:none}

/* ---------- sections ---------- */
section{padding-top:38px}
.sec-h{display:flex;align-items:flex-start;gap:16px;margin-bottom:6px}
.sec-h .num{flex:0 0 auto;min-width:52px;height:52px;border-radius:12px;background:var(--navy);color:#fff;
  display:flex;align-items:center;justify-content:center;font-size:19px;font-weight:800;
  font-variant-numeric:tabular-nums}
.sec-h.mod .num{background:linear-gradient(135deg,#1b4f86,#123b67)}
.sec-h h2{font-size:clamp(21px,2.4vw,29px);margin-top:4px}
.sec-kick{font-size:12px;letter-spacing:.14em;color:var(--blue);font-weight:800;margin-bottom:6px;text-transform:uppercase}
.sec-lead{font-size:16px;color:var(--body);max-width:960px;margin:10px 0 4px}
h3{font-size:18.5px;margin:34px 0 10px;padding-bottom:7px;border-bottom:1px solid var(--line2)}
h3 .hn{color:var(--blue);font-variant-numeric:tabular-nums;margin-right:9px;font-weight:800}
h4{font-size:15px;margin:22px 0 8px;color:var(--navy2);letter-spacing:.01em}
h5{font-size:13px;margin:18px 0 6px;color:var(--muted);letter-spacing:.08em;text-transform:uppercase}
p{margin:0 0 12px;max-width:100ch}
section>hr{border:0;border-top:1px solid var(--line2);margin:34px 0}
ul,ol{margin:0 0 14px;padding-left:22px;max-width:100ch}
li{margin-bottom:6px}
li::marker{color:var(--skyb)}
ul.tick{list-style:none;padding-left:2px}
ul.tick>li{position:relative;padding-left:26px;margin-bottom:7px}
ul.tick>li:before{content:"";position:absolute;left:0;top:.42em;width:14px;height:14px;border-radius:4px;
  border:1.6px solid var(--skyb);background:#fff}
ul.tick>li:after{content:"";position:absolute;left:4px;top:.52em;width:6px;height:9px;
  border-right:2px solid var(--blue);border-bottom:2px solid var(--blue);transform:rotate(42deg);opacity:.55}
ol.num{counter-reset:n;list-style:none;padding-left:0}
ol.num>li{counter-increment:n;position:relative;padding-left:38px;margin-bottom:10px}
ol.num>li:before{content:counter(n);position:absolute;left:0;top:.12em;width:24px;height:24px;border-radius:50%;
  background:var(--sky);color:var(--blue);font-weight:800;font-size:12px;display:flex;align-items:center;justify-content:center;
  border:1px solid var(--skyb)}

/* ---------- tables ---------- */
.tw{overflow-x:auto;margin:14px 0 20px;border:1px solid var(--line);border-radius:12px;background:#fff}
table{border-collapse:collapse;width:100%;font-size:13.6px;line-height:1.5}
caption{caption-side:top;text-align:left;font-size:11.5px;letter-spacing:.1em;color:var(--faint);
  font-weight:800;text-transform:uppercase;padding:0 0 8px}
thead th{background:var(--navy);color:#fff;font-weight:700;font-size:12.2px;letter-spacing:.045em;
  text-align:left;padding:11px 14px;border-right:1px solid rgba(255,255,255,.14);white-space:nowrap}
thead th:last-child{border-right:0}
tbody td{padding:10px 14px;border-top:1px solid var(--line2);vertical-align:top;color:var(--body)}
tbody tr:nth-child(even){background:#fafbfd}
tbody tr:hover{background:var(--sky)}
tbody td:first-child{color:var(--navy);font-weight:700}
td.c,th.c{text-align:center}
table.plain tbody td:first-child{font-weight:600;color:var(--body)}
.tnote{font-size:12px;color:var(--faint);margin:-12px 0 20px;padding-left:2px}

/* ---------- callouts ---------- */
.box{border:1px solid var(--line);border-left:5px solid var(--blue);border-radius:10px;
  padding:15px 18px 13px;margin:18px 0;background:#fbfcfe;break-inside:avoid}
.box .lbl{font-size:11px;letter-spacing:.14em;font-weight:800;color:var(--blue);margin-bottom:6px;text-transform:uppercase}
.box p:last-child,.box ul:last-child,.box ol:last-child{margin-bottom:0}
.box.key{border-left-color:var(--navy);background:#f6f8fc}
.box.key .lbl{color:var(--navy)}
.box.warn{border-left-color:var(--amberb);background:#fffdf5}
.box.warn .lbl{color:#8a6410}
.box.risk{border-left-color:var(--redb);background:#fffbfb}
.box.risk .lbl{color:#7d2b30}
.box.ok{border-left-color:var(--greenb);background:#f8fcf9}
.box.ok .lbl{color:#1f6b3c}
.box code{background:#fff}

/* ---------- figures ---------- */
figure{margin:22px 0 26px;break-inside:avoid}
.figframe{border:1px solid var(--line);border-radius:14px;padding:12px;background:#fff;
  box-shadow:0 12px 34px -26px rgba(15,43,76,.5);overflow-x:auto}
figure svg{display:block;margin:0 auto}
figcaption{font-size:12.5px;color:var(--muted);margin-top:11px;padding-left:2px;line-height:1.55}
figcaption b{color:var(--navy);font-weight:700}

/* ---------- cards / grids ---------- */
.grid{display:grid;gap:14px;margin:16px 0 22px}
.g2{grid-template-columns:repeat(auto-fit,minmax(310px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.g4{grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}
.card{border:1px solid var(--line);border-radius:12px;padding:15px 16px;background:#fff;break-inside:avoid}
.card h4{margin:0 0 7px;font-size:14px}
.card p{font-size:13.2px;margin:0;color:var(--muted);line-height:1.55}
.card.accent{border-top:3px solid var(--blue)}
.card ul{margin:6px 0 0;padding-left:18px;font-size:13.2px;color:var(--body)}
.kpi{border:1px solid var(--line);border-radius:12px;padding:14px 16px;background:linear-gradient(180deg,#fff,#fafbfd)}
.kpi .v{font-size:26px;font-weight:800;color:var(--navy);line-height:1.1;letter-spacing:-.02em}
.kpi .k{font-size:11px;letter-spacing:.11em;color:var(--faint);font-weight:800;text-transform:uppercase;margin-bottom:5px}
.kpi .d{font-size:12.3px;color:var(--muted);margin-top:6px;line-height:1.5}

/* ---------- chips & badges ---------- */
.pill{display:inline-block;font-size:11px;font-weight:800;letter-spacing:.06em;padding:2.5px 9px;border-radius:99px;
  background:var(--sky);color:var(--blue);border:1px solid var(--skyb);white-space:nowrap}
.pill.g{background:var(--green);color:#1f6b3c;border-color:#b7dfc4}
.pill.a{background:var(--amber);color:#8a6410;border-color:#ecd59a}
.pill.r{background:var(--red);color:#7d2b30;border-color:#f0c3c6}
.pill.n{background:var(--grey);color:var(--muted);border-color:var(--line)}
.raci{display:inline-block;min-width:26px;text-align:center;font-size:11.5px;font-weight:800;padding:2px 6px;border-radius:6px}
.raci.A{background:var(--red);color:#7d2b30}
.raci.R{background:var(--sky);color:var(--blue)}
.raci.C{background:var(--grey);color:var(--muted)}
.raci.I{background:#fff;color:#a4b0be;border:1px solid var(--line)}

/* ---------- checklists ---------- */
.ck{width:100%;border-collapse:separate;border-spacing:0}
.ck thead th{position:sticky;top:0;z-index:2}
.ck tbody td{padding:8px 12px}
.ck tbody td:first-child{font-weight:600;color:var(--ink);width:38px;text-align:center}
.ck .item{font-weight:600;color:var(--ink)}
.ck input[type=checkbox]{width:17px;height:17px;accent-color:var(--blue);cursor:pointer;margin:0}
.ck select,.ck input[type=text]{font-family:inherit;font-size:12.8px;border:1px solid var(--line);
  border-radius:7px;padding:5px 8px;width:100%;background:#fff;color:var(--body)}
.ck select:focus,.ck input[type=text]:focus{outline:2px solid var(--skyb);border-color:var(--blue)}
.ck tr.done{background:#f4fbf6 !important}
.ck tr.done .item{color:#1f6b3c}
.ckbar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 10px;font-size:12.5px;color:var(--muted)}
.ckbar .meter{flex:1 1 160px;height:7px;background:var(--line2);border-radius:4px;overflow:hidden;min-width:120px}
.ckbar .meter i{display:block;height:100%;width:0;background:linear-gradient(90deg,#4d90d4,#3d9a5f);transition:width .2s}
.ck-tools{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin:10px 0 26px;font-size:12.5px}

/* ---------- QA / accordion ---------- */
details{border:1px solid var(--line);border-radius:11px;margin-bottom:11px;background:#fff;break-inside:avoid}
details[open]{border-color:var(--skyb);box-shadow:0 8px 22px -18px rgba(15,43,76,.6)}
summary{cursor:pointer;padding:13px 16px;font-weight:700;color:var(--navy);font-size:14.5px;list-style:none;
  display:flex;gap:12px;align-items:flex-start}
summary::-webkit-details-marker{display:none}
summary .qn{flex:0 0 auto;min-width:26px;height:26px;border-radius:8px;background:var(--sky);color:var(--blue);
  font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center;border:1px solid var(--skyb)}
summary .car{margin-left:auto;color:var(--faint);font-size:12px;transition:transform .2s;flex:0 0 auto;padding-top:5px}
details[open] summary .car{transform:rotate(90deg)}
details .ans{padding:0 16px 15px 54px;font-size:14px;color:var(--body)}
details .ans p{margin-bottom:8px}

/* ---------- misc ---------- */
.flowline{display:flex;flex-wrap:wrap;align-items:center;gap:7px;margin:14px 0 20px;padding:14px 16px;
  background:linear-gradient(180deg,#f8fafd,#fff);border:1px solid var(--line);border-radius:12px}
.flowline b{font-size:13.2px;color:var(--navy);font-weight:700;background:#fff;border:1px solid var(--skyb);
  padding:5px 11px;border-radius:8px}
.flowline i{color:var(--skyb);font-style:normal;font-weight:800}
.cmd{background:#0e2340;color:#d6e4f5;border-radius:11px;padding:13px 16px;margin:12px 0 18px;
  font-family:var(--mono);font-size:12.6px;line-height:1.75;overflow-x:auto;break-inside:avoid}
.cmd .c{color:#6f8fb3}
.cmd .p{color:#8fd6a8}
.cmd b{color:#fff;font-weight:700}
.tocprint{display:none}
.backtop{position:fixed;right:22px;bottom:22px;z-index:60;width:44px;height:44px;border-radius:50%;
  background:var(--navy);color:#fff;border:0;cursor:pointer;font-size:18px;box-shadow:0 10px 24px -10px rgba(15,43,76,.8);
  opacity:0;pointer-events:none;transition:opacity .2s}
.backtop.on{opacity:.94;pointer-events:auto}
@media (max-width:1080px){.rail{display:none}.paper{box-shadow:none}}

/* ---------- print ---------- */
@page{size:A4;margin:17mm 15mm 18mm}
@page:first{margin:0}
@media print{
  body{background:#fff;font-size:10.4pt;line-height:1.5;color:#1b2b3a}
  .rail,.topbar,.backtop,.ck-tools .btn,.no-print{display:none !important}
  .shell{display:block;max-width:none}
  .paper{box-shadow:none;border:0}
  .wrap{padding:0}
  .cover{padding:26mm 18mm 16mm;-webkit-print-color-adjust:exact;print-color-adjust:exact;
    page-break-after:always;min-height:262mm}
  .rhead{display:block;position:running(rh);}
  section{padding-top:0;page-break-before:always}
  section.nobreak{page-break-before:auto}
  h2,h3,h4{page-break-after:avoid;break-after:avoid}
  figure,.box,.card,.tw,table,.cmd,details{page-break-inside:avoid;break-inside:avoid}
  .figframe{box-shadow:none;border-color:#c9d4e0}
  .tocprint{display:block}
  a{color:#123a63}
  .tw{overflow:visible;border-color:#c9d4e0}
  thead th{background:#0f2b4c !important;color:#fff !important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  tbody tr:nth-child(even){background:#f6f8fb !important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .box,.pill,.kpi,.card,.cmd,.cover,.raci{-webkit-print-color-adjust:exact;print-color-adjust:exact}
  details{border-color:#c9d4e0}
  details .ans{display:block !important}
  details summary .car{display:none}
  input[type=checkbox]{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
"""

JS = r"""
(function(){
  var KEY='sap-mig-handbook-v1';
  var state={};
  try{state=JSON.parse(localStorage.getItem(KEY)||'{}');}catch(e){state={};}
  function save(){try{localStorage.setItem(KEY,JSON.stringify(state));}catch(e){}}

  // ---- checkbox persistence + row state + meters
  document.querySelectorAll('.ck').forEach(function(tb){
    var box=tb.closest('figure')||tb.closest('section')||document;
    var meter=box.querySelector('.meter i');
    var pct=box.querySelector('.pct');
    function refresh(){
      var all=tb.querySelectorAll('input[type=checkbox]'),done=0;
      all.forEach(function(cb){
        var tr=cb.closest('tr'); if(!tr)return;
        tr.classList.toggle('done',cb.checked); if(cb.checked)done++;
      });
      if(meter&&all.length)meter.style.width=(done/all.length*100)+'%';
      if(pct&&all.length)pct.textContent=done+' of '+all.length+' complete ('+Math.round(done/all.length*100)+'%)';
    }
    tb.querySelectorAll('input[type=checkbox]').forEach(function(cb,i){
      var id=cb.getAttribute('data-id')||( (tb.getAttribute('data-list')||'list')+'-'+i );
      cb.setAttribute('data-id',id);
      if(state[id])cb.checked=true;
      cb.addEventListener('change',function(){
        if(cb.checked)state[id]=1;else delete state[id];
        save();refresh();refreshRail();
      });
    });
    tb.querySelectorAll('input[type=text],select').forEach(function(f,i){
      var id=f.getAttribute('data-id')||((tb.getAttribute('data-list')||'list')+'-f'+i);
      f.setAttribute('data-id',id);
      if(state[id]&&typeof state[id]==='string')f.value=state[id];
      f.addEventListener('change',function(){state[id]=f.value;save();});
    });
    refresh();
  });

  function clearList(sel){
    document.querySelectorAll(sel+' input[type=checkbox]').forEach(function(cb){cb.checked=false;delete state[cb.getAttribute('data-id')];});
    document.querySelectorAll(sel+' input[type=text]').forEach(function(f){f.value='';delete state[f.getAttribute('data-id')];});
    save();
    document.querySelectorAll(sel+'.ck, '+sel+' .ck').forEach(function(tb){
      tb.querySelectorAll('tr').forEach(function(tr){tr.classList.remove('done');});
    });
    location.reload();
  }
  document.querySelectorAll('[data-reset]').forEach(function(b){
    b.addEventListener('click',function(){clearList(b.getAttribute('data-reset'));});
  });

  // ---- rail progress + scrollspy
  var links=[].slice.call(document.querySelectorAll('.rail nav a[href^="#"]'));
  function refreshRail(){
    var all=document.querySelectorAll('.ck input[type=checkbox]');
    var done=0;all.forEach(function(cb){if(cb.checked)done++;});
    var p=all.length?done/all.length:0;
    var bar=document.querySelector('.rail .prog i');
    var txt=document.querySelector('.rail .progtxt');
    if(bar)bar.style.width=(p*100)+'%';
    if(txt)txt.textContent=all.length?('Checklist progress: '+done+' / '+all.length+' ('+Math.round(p*100)+'%)'):'Checklists not started';
  }
  var secs=[].slice.call(document.querySelectorAll('section[id]'));
  function spy(){
    var y=window.scrollY+140,cur=null;
    secs.forEach(function(s){if(s.offsetTop<=y)cur=s.id;});
    links.forEach(function(a){a.classList.toggle('active',a.getAttribute('href')==='#'+cur);});
    var bt=document.querySelector('.backtop');
    if(bt)bt.classList.toggle('on',window.scrollY>700);
  }
  window.addEventListener('scroll',spy,{passive:true});
  refreshRail();spy();

  // ---- expand / collapse all Q&A
  document.querySelectorAll('[data-expand]').forEach(function(b){
    b.addEventListener('click',function(){
      var open=b.getAttribute('data-expand')==='1';
      document.querySelectorAll(b.getAttribute('data-scope')+' details').forEach(function(d){d.open=open;});
    });
  });
  document.querySelectorAll('[data-print]').forEach(function(b){
    b.addEventListener('click',function(){
      document.querySelectorAll('details').forEach(function(d){d.open=true;});
      window.print();
    });
  });
  var bt=document.querySelector('.backtop');
  if(bt)bt.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});
})();
"""
