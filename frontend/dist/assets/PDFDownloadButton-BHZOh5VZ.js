import{h as v,E as M}from"./pdf-B39ievqC.js";import{_ as R}from"./index-Egejfov0.js";import{a as A,b as P,o as T,d as B,a1 as I,t as N,n as G}from"./vendor-D171CWhe.js";function $(t){t.saveGraphicsState(),t.setTextColor(200,200,200),t.setFontSize(50),t.setFont("times","bold");const o=105,e=148,n=-45*(Math.PI/180);t.text("OptiTAB",o,e,{angle:n,align:"center"}),t.restoreGraphicsState()}function k(t,o,e){t.setFontSize(9),t.setTextColor(107,114,128),t.setFont("times","normal"),t.text("OptiTAB - Plateforme éducative",15,280),t.text(`Page ${o} / ${e}`,195,280,{align:"right"})}function D(t,o,e){const n=[],a=t.width/o,l=Math.floor(e*a),g=Math.floor(a*8),p=t.getContext("2d"),c=t.width,d=t.height,u=Math.max(40,Math.floor(a*4)),w=Math.max(3,Math.floor(c*.004));function m(f){const r=p.getImageData(0,f,c,1).data;let s=0;for(let i=0;i<c;i+=4){const x=i*4,E=r[x],j=r[x+1],O=r[x+2];if(r[x+3]>0&&(E<245||j<245||O<245)&&(s++,s>w))return!1}return!0}function b(f){for(let r=0;r<=u;r++){const s=Math.min(d-1,f+r);if(m(s))return s;const i=Math.max(0,f-r);if(m(i))return i}return Math.min(d,Math.max(0,f))}let h=0;for(;h<d;){const f=h+l>=d;let r;if(f)r=d;else{const E=h+l-g;r=b(E),r<=h+40&&(r=Math.min(d,h+l))}const s=Math.min(r-h,d-h),i=document.createElement("canvas");i.width=c,i.height=s,i.getContext("2d").drawImage(t,0,h,c,s,0,0,c,s),n.push(i),h+=s}return n}async function C(t){if(await(async()=>{if(!(typeof window>"u"||!window.MathJax)&&window.MathJax.startup&&window.MathJax.startup.promise)try{await window.MathJax.startup.promise}catch{}})(),typeof window<"u"&&window.MathJax&&window.MathJax.typesetPromise)try{await window.MathJax.typesetPromise([t]),t.querySelectorAll("mjx-assistive-mml, .MJX_Assistive_MathML").forEach(e=>e.parentNode&&e.parentNode.removeChild(e)),await new Promise(e=>setTimeout(e,700))}catch{}}function L(t,o=!1){const e=document.createElement("div");return e.style.cssText=`
    position: absolute;
    top: -9999px;
    left: -9999px;
    width: 210mm;
    background: white;
    font-family: 'Times New Roman', serif;
    font-size: 12px;
    line-height: 1.6;
    color: #000;
    padding: 20px;
    box-sizing: border-box;
  `,e.innerHTML=t,document.body.appendChild(e),e}function y(t){return t?t.replace(/&lt;/g,"<").replace(/&gt;/g,">").replace(/&amp;/g,"&").replace(/\n\n/g,"<br/><br/>").replace(/\n/g,"<br/>").replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>").replace(/\*([^*]+)\*/g,"<em>$1</em>"):""}function F(t,o=!0){const e=t.titre||t.nom||`Exercice ${t.id||""}`,n=y(t.question||t.instruction||t.contenu||""),a=y(t.reponse_correcte||t.solution||""),l=y(t.etapes||"");return`
    <div class="exercice-container">
      <div class="exercice-header">
        <h2 class="exercice-titre">${e}</h2>
        ${t.points?`<div class="exercice-points">${t.points} point(s)</div>`:""}
      </div>
      
      <div class="section enonce-section">
        <h3 class="section-title">📋 Énoncé</h3>
        <div class="section-content">${n}</div>
      </div>
      
      ${o&&l?`
      <div class="section etapes-section">
        <h3 class="section-title">🔢 Méthode de résolution</h3>
        <div class="section-content">${l}</div>
      </div>
      `:""}
      
      ${o&&a?`
      <div class="section solution-section">
        <h3 class="section-title">✅ Solution</h3>
        <div class="section-content">${a}</div>
      </div>
      `:""}
    </div>
  `}function W(t){const o=t.titre||`Cours ${t.id||""}`,e=t.description||"",n=y(t.contenu||""),a=t.difficulty||"medium";return`
    <div class="cours-container">
      <div class="cours-header">
        <h2 class="cours-titre">${o}</h2>
        <div class="cours-difficulty ${a}">${{easy:"Facile",medium:"Moyen",hard:"Difficile"}[a]||a}</div>
      </div>
      
      ${e?`
      <div class="section description-section">
        <h3 class="section-title">📖 Description</h3>
        <div class="section-content">${y(e)}</div>
      </div>
      `:""}
      
      <div class="section contenu-section">
        <h3 class="section-title">📚 Contenu du cours</h3>
        <div class="section-content">${n}</div>
      </div>
    </div>
  `}function _(){return`
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      
      body {
        font-family: 'Times New Roman', serif;
        font-size: 12px;
        line-height: 1.6;
        color: #1f2937;
        background: white;
        padding: 20px;
      }
      
      /* Masquer les contenus d'accessibilité MathJax (évite les doublons) */
      mjx-assistive-mml, .MJX_Assistive_MathML { display: none !important; }
      
      .pdf-header {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: #1e40af;
        margin-bottom: 30px;
        padding-bottom: 15px;
        border-bottom: 3px solid #1e40af;
      }
      
      .exercice-container {
        margin-bottom: 40px;
        page-break-inside: avoid;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        background: #fafbfc;
      }
      
      .cours-container {
        margin-bottom: 40px;
        page-break-inside: avoid;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        background: #fafbfc;
      }
      
      .exercice-header {
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid #3b82f6;
      }
      
      .cours-header {
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid #10b981;
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
      }
      
      .exercice-titre {
        font-size: 16px;
        font-weight: bold;
        color: #1e40af;
        margin-bottom: 5px;
      }
      
      .cours-titre {
        font-size: 16px;
        font-weight: bold;
        color: #1e40af;
        margin-bottom: 5px;
        flex: 1;
      }
      
      .cours-difficulty {
        padding: 4px 8px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }
      
      .cours-difficulty.easy {
        background: #e8f5e8;
        color: #2e7d32;
      }
      
      .cours-difficulty.medium {
        background: #fff3e0;
        color: #f57c00;
      }
      
      .cours-difficulty.hard {
        background: #ffebee;
        color: #c62828;
      }
      
      .exercice-points {
        font-size: 11px;
        color: #6b7280;
        background: #f3f4f6;
        padding: 3px 8px;
        border-radius: 10px;
        display: inline-block;
      }
      
      .section {
        margin-bottom: 18px;
        page-break-inside: avoid;
      }
      
      .section-title {
        font-size: 13px;
        font-weight: bold;
        color: #374151;
        margin-bottom: 8px;
        padding: 6px 10px;
        background: #f1f5f9;
        border-left: 4px solid #3b82f6;
        border-radius: 4px;
      }
      
      .etapes-section .section-title {
        border-left-color: #8b5cf6;
        background: #faf5ff;
      }
      
      .solution-section .section-title {
        border-left-color: #10b981;
        background: #f0fdf4;
      }
      
      .section-content {
        padding: 12px;
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        line-height: 1.8;
      }
      
      /* Styles pour MathJax */
      .MathJax, mjx-container {
        margin: 8px 0 !important;
        page-break-inside: avoid;
      }
      
      .MathJax_Display {
        margin: 12px 0 !important;
        text-align: center;
      }
      
      /* Images */
      img {
        max-width: 100%;
        height: auto;
        page-break-inside: avoid;
        border-radius: 4px;
        margin: 8px 0;
      }
      
      /* Formatage du texte */
      strong { color: #1f2937; font-weight: bold; }
      em { color: #374151; font-style: italic; }
      
      /* Éviter les coupures */
      .no-break { page-break-inside: avoid; }
    </style>
  `}async function H(t,o="exercice",e=!0,n=!1){try{const a=t.titre||t.nom||"Exercice",l=_(),g=F(t,n),p=`
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        ${l}
      </head>
      <body>
        <div class="pdf-header">${a} - Exercice complet</div>
        ${g}
      </body>
      </html>
    `,c=L(p,e);e&&await C(c);const d=await v(c,{scale:2,useCORS:!0,allowTaint:!0,backgroundColor:"#ffffff",width:794,height:1123});document.body.removeChild(c);const u=new M("portrait","mm","a4"),w=5,m=12,b=200,f=D(d,b,250),r=f.length;let s=1;f.forEach((i,x)=>{x>0&&u.addPage(),u.addImage(i.toDataURL("image/jpeg",.95),"JPEG",w,m,b,i.height*b/i.width),$(u),k(u,s,r),s++}),u.save(`${o}.pdf`)}catch(a){throw a}}async function J(t,o="exercices",e=!0,n=!1){try{if(!Array.isArray(t)||t.length===0)throw new Error("Aucun exercice à exporter");const a=n?`Exercices avec solutions (${t.length} exercice(s))`:`Exercices - énoncés seuls (${t.length} exercice(s))`,l=_(),g=t.map(i=>F(i,n)).join(""),p=`
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        ${l}
      </head>
      <body>
        <div class="pdf-header">${a}</div>
        ${g}
      </body>
      </html>
    `,c=L(p,!0);e&&await C(c);const d=await v(c,{scale:2,useCORS:!0,allowTaint:!0,backgroundColor:"#ffffff",width:794});document.body.removeChild(c);const u=new M("portrait","mm","a4"),w=5,m=12,b=200,f=D(d,b,250),r=f.length;let s=1;f.forEach((i,x)=>{x>0&&u.addPage(),u.addImage(i.toDataURL("image/jpeg",.95),"JPEG",w,m,b,i.height*b/i.width),$(u),k(u,s,r),s++}),u.save(`${o}.pdf`)}catch(a){throw a}}async function S(t,o="cours",e=!0){try{if(!Array.isArray(t)||t.length===0)throw new Error("Aucun cours à exporter");const n=`Cours (${t.length} cours)`,a=_(),l=t.map(s=>W(s)).join(""),g=`
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        ${a}
      </head>
      <body>
        <div class="pdf-header">${n}</div>
        ${l}
      </body>
      </html>
    `,p=L(g,!0);e&&await C(p);const c=await v(p,{scale:2,useCORS:!0,allowTaint:!0,backgroundColor:"#ffffff",width:794});document.body.removeChild(p);const d=new M("portrait","mm","a4"),u=5,w=12,m=200,h=D(c,m,250),f=h.length;let r=1;h.forEach((s,i)=>{i>0&&d.addPage(),d.addImage(s.toDataURL("image/jpeg",.95),"JPEG",u,w,m,s.height*m/s.width),$(d),k(d,r,f),r++}),d.save(`${o}.pdf`)}catch(n){throw n}}async function z(t,o="document.pdf",e={}){try{const n=await v(t,{scale:2,useCORS:!0,allowTaint:!0,backgroundColor:"#ffffff",...e}),a=new M("portrait","mm","a4"),l=210,g=297,p=n.height*l/n.width;let c=p,d=0;for(a.addImage(n.toDataURL("image/jpeg",.95),"JPEG",0,d,l,p),c-=g;c>=0;)d=c-p,a.addPage(),a.addImage(n.toDataURL("image/jpeg",.95),"JPEG",0,d,l,p),c-=g;a.save(o)}catch(n){throw n}}const et=Object.freeze(Object.defineProperty({__proto__:null,generateCoursPDF:S,generateExercicePDF:H,generateExercicesListPDF:J,generatePDFFromHTML:z},Symbol.toStringTag,{value:"Module"})),q=["disabled"],U={key:0,class:"loading-spinner"},Y={key:1,class:"pdf-icon",width:"16",height:"16",viewBox:"0 0 24 24",fill:"none",stroke:"currentColor","stroke-width":"2"},V={class:"btn-text"},X={__name:"PDFDownloadButton",props:{type:{type:String,default:"single",validator:t=>["single","list","html","cours"].includes(t)},data:{type:[Object,Array],required:!0},title:{type:String,default:"Document"},text:{type:String,default:"Télécharger PDF"},htmlElement:{type:HTMLElement,default:null},options:{type:Object,default:()=>({})},useMathJax:{type:Boolean,default:!1},includeSolution:{type:Boolean,default:!1}},setup(t){const o=t,e=A(!1);async function n(){if(!e.value){e.value=!0;try{switch(o.type){case"single":await H(o.data,o.title,o.useMathJax,o.includeSolution);break;case"list":await J(o.data,o.title,o.useMathJax,o.includeSolution);break;case"html":if(!o.htmlElement)throw new Error('Élément HTML requis pour le type "html"');await z(o.htmlElement,`${o.title}.pdf`,o.options);break;case"cours":await S(o.data,o.title,o.useMathJax);break;default:throw new Error(`Type de téléchargement non supporté: ${o.type}`)}}catch{alert("Erreur lors de la génération du PDF. Veuillez réessayer.")}finally{e.value=!1}}}return(a,l)=>(T(),P("button",{class:G(["pdf-download-btn",{loading:e.value}]),onClick:n,disabled:e.value},[e.value?(T(),P("span",U)):(T(),P("svg",Y,l[0]||(l[0]=[I('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" data-v-cb561f51></path><polyline points="14,2 14,8 20,8" data-v-cb561f51></polyline><line x1="16" y1="13" x2="8" y2="13" data-v-cb561f51></line><line x1="16" y1="17" x2="8" y2="17" data-v-cb561f51></line><polyline points="10,9 9,9 8,9" data-v-cb561f51></polyline>',5)]))),B("span",V,N(e.value?"Génération...":t.text),1)],10,q))}},ot=R(X,[["__scopeId","data-v-cb561f51"]]);export{ot as P,et as p};
