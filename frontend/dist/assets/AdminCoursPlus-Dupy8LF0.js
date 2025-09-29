import{a as p,c as tt,e as et,b as d,ap as it,d as a,i as h,m as M,K as U,N as ot,F as k,s as T,t as g,B as rt,o as u,n as S,l as nt}from"./vendor-CH-G3qaL.js";import{_ as at}from"./index-CTBwyioG.js";import{a as lt,f as st}from"./curriculum-BDGRPb8j.js";import{g as dt,u as ut,a as gt,c as ct}from"./cours-BrcUnH7F.js";import{r as pt,a as ft}from"./scientificRenderer-B77YcBUU.js";import"./ui-jaH5oyHW.js";import"./pdf-S6SQ1w6P.js";import"./mathlive-B5k0jhbN.js";const mt={class:"bulk-form"},vt=["value"],ht={class:"images-upload-section"},xt={key:0,class:"selected-images"},bt=["src","alt"],yt={class:"image-name"},qt=["onClick"],It={class:"btn-group"},Ct=["disabled"],Et=["disabled"],_t={key:0,class:"success-msg"},$t={key:1,class:"error-msg"},At={key:2,class:"info-msg"},kt={key:3,class:"preview-section"},Tt={key:0,class:"preview-image-info"},Nt={class:"image-indicator"},Lt={class:"image-status-list"},Mt={class:"preview-cours"},wt={class:"preview-header"},Dt={class:"ordre-badge"},Ot={key:0,class:"preview-description"},Pt=["innerHTML"],Rt=10*1024*1024,Ut={__name:"AdminCoursPlus",setup(St){const j=["image/jpeg","image/jpg","image/png","image/gif","image/webp","image/svg+xml"],q=p([]),_=p([]),$=p(""),c=p(""),v=p(""),N=p(""),m=p(""),x=p([]),w=p(!1),b=p([]),L=p(null);class z{constructor(){this.images=new Map}addImage(e){if(!this.validateImage(e))throw new Error(`Image invalide: ${e.name}`);this.images.set(e.name,e)}removeImage(e){this.images.delete(e)}validateImage(e){return!(!j.includes(e.type)||e.size>Rt)}getImage(e){return this.images.get(e)}getImageNames(){return Array.from(this.images.keys())}}const I=new z;function D(i){return _.value.find(e=>String(e.id)===String(i))}function F(i){if(!i)return null;const e=D(i.notion);if(!e)return{themeNom:"",matiereNom:"",paysNom:"",niveauNom:""};const t=e.matiere_nom||e.contexte_detail&&e.contexte_detail.matiere_nom||"",n=e.theme_nom||"",r=e.contexte_detail&&e.contexte_detail.pays?e.contexte_detail.pays.nom:"",l=e.contexte_detail&&e.contexte_detail.niveau?e.contexte_detail.niveau.nom:"";return{matiereNom:t,themeNom:n,paysNom:r,niveauNom:l}}function O(i){const e=D(i.notion),t=F(i);return[i.nom,e?`— ${e.nom}`:"",t&&t.matiereNom?`— ${t.matiereNom}`:"",t&&(t.paysNom||t.niveauNom)?`— ${[t.paysNom,t.niveauNom].filter(Boolean).join(" · ")}`:""].filter(Boolean).join(" ")}function V(i){return{easy:"Facile",medium:"Moyen",hard:"Difficile"}[i]||i}function B(i){return URL.createObjectURL(i)}function A(i){return I.getImage(i)}function G(i,e=null){return(i||"").split(",").map(n=>n.trim()).filter(Boolean).map((n,r)=>{const l=A(n);return{id:`preview-${r}`,image:l?URL.createObjectURL(l):n,image_type:"illustration",position:r+1}})}function W(i){const e=G(i.image,i);let t=i.contenu;const n=(i.image||"").split(",").map(r=>r.trim()).filter(Boolean);if(t=t.replace(/\[IMAGE_(\d+)\]/g,(r,l)=>{const o=parseInt(l)-1,s=n[o],f=A(s);return f?`
        <div class="preview-image-container" style="text-align: center; margin: 2em 0;">
          <img src="${URL.createObjectURL(f)}" alt="Image ${l}" class="content-image" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
          <div class="image-info" style="margin-top: 0.5rem; font-size: 0.875rem; color: #28a745; font-weight: 500;">✅ ${s}</div>
        </div>
      `:`
        <div class="preview-image-placeholder">
          <div class="placeholder-icon">🖼️</div>
          <div class="placeholder-text">Image manquante: ${s||`IMAGE_${l}`}</div>
          <div class="placeholder-hint">Uploadez cette image dans la section ci-dessus</div>
        </div>
      `}),!/\[IMAGE_\d+\]/.test(i.contenu||"")&&e.length>0){const r=e.map(l=>`
      <div class="content-image-container" style="text-align: center; margin: 2em 0;">
        <img 
          src="${l.image}" 
          alt="Image ${l.position||""}" 
          class="content-image"
          style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"
        />
      </div>
    `).join(`
`);t=`${t}
${r}`}return ft(t,e)}function H(i){Array.from(i.target.files).forEach(t=>{try{I.addImage(t),b.value.push(t)}catch{}})}function Q(i){const e=b.value[i];I.removeImage(e.name),b.value.splice(i,1)}function P(i){const e=i.split("===").filter(n=>n.trim()),t=[];for(const n of e)try{const r=J(n.trim());r&&t.push(r)}catch{}return t}function J(i){const e=i.split(`
`),t={titre:"",description:"",contenu:"",difficulty:"medium",ordre:0,image:"",chapitre:c.value,matiere:null,notion:null};if(c.value){const l=q.value.find(o=>o.id==c.value);if(l){const o=_.value.find(s=>s.id==l.notion);o&&(t.notion=o.id,t.matiere=o.matiere)}}let n="header",r=[];for(let l=0;l<e.length;l++){const o=e[l].trim();o&&(n==="header"?o.startsWith("Difficulté:")?t.difficulty=o.split(":")[1].trim():o.startsWith("Ordre:")?t.ordre=parseInt(o.split(":")[1].trim())||0:o.startsWith("Chapitre:")||(o.toLowerCase().startsWith("image:")||o.toLowerCase().startsWith("images:")?t.image=o.split(":")[1].trim():o.startsWith("Titre:")?t.titre=o.split(":")[1].trim():o.startsWith("Description:")?(t.description=o.split(":")[1].trim(),n="content"):!t.titre&&!o.startsWith("===")&&(t.titre=o)):r.push(o))}return t.contenu=r.join(`
`),!t.titre||!t.contenu||!t.matiere||!t.chapitre?null:t}function X(){try{w.value=!0,x.value=P(v.value),rt(()=>{pt()})}catch{m.value="Erreur lors de la prévisualisation"}}async function K(){if(!c.value){m.value="Veuillez sélectionner un chapitre";return}const i=q.value.find(t=>t.id==c.value);if(!i){m.value="Chapitre invalide";return}if(!_.value.find(t=>t.id==i.notion)){m.value="Notion invalide pour ce chapitre";return}try{const t=P(v.value);if(t.length===0){m.value="Aucun cours valide trouvé";return}let n=0,r=0,l=0,o=null;try{const s=await dt(null,null,Number(c.value)),f=Array.isArray(s?.data)?s.data:Array.isArray(s)?s:[];f&&f.length>0&&(o=f[0].id)}catch{}for(const s of t)try{const f={chapitre:Number(s.chapitre),titre:s.titre,contenu:s.contenu,ordre:s.ordre||0,difficulty:s.difficulty||"medium"};let C;if(o)C=(await ut(o,f))?.id||o,r++;else{const{data:E}=await gt(f);C=E?.id,n++,o=C}if(s.image&&C){const E=s.image.split(",").map(y=>y.trim()).filter(Boolean);for(let y=0;y<E.length;y++){const R=I.getImage(E[y]);if(R){const Z={cours:C,image:R,image_type:"illustration",position:y+1};await ct(Z)}}}}catch{l++}if(n>0||r>0){N.value=`${n} créé(s)${r?`, ${r} mis à jour`:""}${l>0?`, ${l} erreur(s)`:""}`;const s=c.value;v.value="",x.value=[],b.value=[],I.images.clear(),L.value&&(L.value.value=""),c.value=s}else m.value="Aucun cours n'a pu être créé"}catch{m.value="Erreur lors de la création des cours"}}const Y=tt(()=>{if(!$.value)return q.value;const i=$.value.toLowerCase();return q.value.filter(e=>O(e).toLowerCase().includes(i))});return et(async()=>{try{const[i,e]=await Promise.all([lt(),st()]);q.value=Array.isArray(i)?i:i?.data||[],_.value=Array.isArray(e)?e:e?.data||[]}catch{}}),(i,e)=>(u(),d("div",null,[e[8]||(e[8]=it(`<h2 class="admin-title" data-v-d4fcef03>Bulk – Ajout de Cours</h2><div class="format-help" data-v-d4fcef03><h3 data-v-d4fcef03>📋 Format requis :</h3><div class="format-example" data-v-d4fcef03><pre data-v-d4fcef03><code data-v-d4fcef03>=== [NOM DU COURS - SOUS-TITRE]
Difficulté: [easy/medium/hard]
Ordre: [numéro]

Titre: [Titre détaillé du cours]
Description: [Description courte expliquant l&#39;objectif du cours]

&lt;div style=&quot;background:#f9f9f9; padding:20px; border-radius:12px; font-family:Arial, sans-serif; line-height:1.6;&quot;&gt;

    &lt;h2 style=&quot;color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;&quot;&gt;I. Définition&lt;/h2&gt;
    &lt;div style=&quot;background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;&quot;&gt;
        &lt;p&gt;Une &lt;strong&gt;[CONCEPT PRINCIPAL]&lt;/strong&gt; est [définition simple et claire].&lt;/p&gt;
        &lt;div style=&quot;text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;&quot;&gt;
            $$[FORMULE DE BASE OU DEFINITION MATHEMATIQUE]$$
        &lt;/div&gt;
        &lt;p&gt;&lt;strong&gt;Explication :&lt;/strong&gt; [Explication pédagogique du concept]&lt;/p&gt;
    &lt;/div&gt;

    &lt;h2 style=&quot;color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;&quot;&gt;II. [CONCEPT THEORIQUE PRINCIPAL]&lt;/h2&gt;
    &lt;div style=&quot;background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;&quot;&gt;
        &lt;p&gt;[Explication du concept théorique principal]&lt;/p&gt;
        &lt;div style=&quot;text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;&quot;&gt;
            $$[FORMULE PRINCIPALE A RETENIR]$$
        &lt;/div&gt;
        &lt;p&gt;&lt;strong&gt;💡 [CONSEIL IMPORTANT] :&lt;/strong&gt; [Conseil méthodologique]&lt;/p&gt;
    &lt;/div&gt;

    &lt;h2 style=&quot;color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;&quot;&gt;III. Exemples détaillés&lt;/h2&gt;

    &lt;div style=&quot;background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;&quot;&gt;
        &lt;h3 style=&quot;color:#34495e; margin-top:0;&quot;&gt;Exemple 1 : [TITRE SPECIFIQUE]&lt;/h3&gt;
        &lt;p&gt;&lt;strong&gt;Énoncé :&lt;/strong&gt; [Description de l&#39;exemple]&lt;/p&gt;
        &lt;p&gt;&lt;strong&gt;Données :&lt;/strong&gt; [Valeurs numériques ou paramètres]&lt;/p&gt;

        &lt;p&gt;&lt;strong&gt;Résolution :&lt;/strong&gt;&lt;/p&gt;
        &lt;div style=&quot;background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;&quot;&gt;
            &lt;ul style=&quot;margin:0; padding-left:20px;&quot;&gt;
                &lt;li&gt;$[Première étape de calcul]$&lt;/li&gt;
                &lt;li&gt;$[Deuxième étape de calcul]$&lt;/li&gt;
                &lt;li&gt;$[Troisième étape de calcul]$&lt;/li&gt;
                &lt;li&gt;$[Conclusion de l&#39;étape]$&lt;/li&gt;
            &lt;/ul&gt;
        &lt;/div&gt;

        &lt;div style=&quot;background:#ecf0f1; padding:10px; border-radius:4px; margin:10px 0;&quot;&gt;
            &lt;strong&gt;Résultat final :&lt;/strong&gt; [Conclusion de l&#39;exemple]
        &lt;/div&gt;
    &lt;/div&gt;

    &lt;div style=&quot;background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;&quot;&gt;
        &lt;h3 style=&quot;color:#34495e; margin-top:0;&quot;&gt;Exemple 2 : [TITRE SPECIFIQUE]&lt;/h3&gt;
        &lt;p&gt;&lt;strong&gt;Situation :&lt;/strong&gt; [Contexte de l&#39;exemple]&lt;/p&gt;

        &lt;div style=&quot;text-align:center; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;&quot;&gt;
            $$[APPLICATION DE LA FORMULE]$$
        &lt;/div&gt;

        &lt;p&gt;&lt;strong&gt;Calculs détaillés :&lt;/strong&gt;&lt;/p&gt;
        &lt;div style=&quot;background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;&quot;&gt;
            &lt;ul style=&quot;margin:0; padding-left:20px;&quot;&gt;
                &lt;li&gt;$[Calcul étape 1]$&lt;/li&gt;
                &lt;li&gt;$[Calcul étape 2]$&lt;/li&gt;
                &lt;li&gt;$[Résultat final]$&lt;/li&gt;
            &lt;/ul&gt;
        &lt;/div&gt;

        &lt;div style=&quot;background:#e8f5e8; padding:8px; border-radius:4px; margin:10px 0;&quot;&gt;
            &lt;strong&gt;✅ Vérification :&lt;/strong&gt; [Vérification du résultat]
        &lt;/div&gt;
    &lt;/div&gt;

    &lt;h2 style=&quot;color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;&quot;&gt;IV. [SECTION D&#39;APPLICATION - CALCULS]&lt;/h2&gt;

    &lt;div style=&quot;background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;&quot;&gt;
        &lt;h3 style=&quot;color:#34495e; margin-top:0;&quot;&gt;[SOUS-TITRE DE LA METHODE]&lt;/h3&gt;
        &lt;p&gt;[Explication de la méthode ou du calcul principal]&lt;/p&gt;

        &lt;div style=&quot;text-align:center; font-size:1.2em; margin:15px 0; padding:12px; background:#f8f9fa; border-radius:4px;&quot;&gt;
            &lt;strong&gt;Formule [NOM DE LA FORMULE] :&lt;/strong&gt;&lt;br&gt;
            $$[FORMULE MATHEMATIQUE PRINCIPALE]$$
        &lt;/div&gt;

        &lt;div style=&quot;background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;&quot;&gt;
            &lt;strong&gt;💡 Démarche à suivre :&lt;/strong&gt;&lt;br&gt;
            • [Étape 1 de la méthode]&lt;br&gt;
            • [Étape 2 de la méthode]&lt;br&gt;
            • [Étape 3 de la méthode]
        &lt;/div&gt;
    &lt;/div&gt;

    &lt;div style=&quot;background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;&quot;&gt;
        &lt;h3 style=&quot;color:#34495e; margin-top:0;&quot;&gt;Application pratique&lt;/h3&gt;
        &lt;p&gt;&lt;strong&gt;Problème :&lt;/strong&gt; [Énoncé du problème d&#39;application]&lt;/p&gt;

        &lt;div style=&quot;background:#f8f9fa; padding:12px; border-radius:4px; margin:10px 0;&quot;&gt;
            &lt;strong&gt;Éléments donnés :&lt;/strong&gt;&lt;br&gt;
            • [Donnée 1]&lt;br&gt;
            • [Donnée 2]&lt;br&gt;
            • [Donnée 3]
        &lt;/div&gt;

        &lt;div style=&quot;text-align:center; margin:15px 0;&quot;&gt;
            &lt;strong&gt;Résolution :&lt;/strong&gt;
            &lt;div style=&quot;font-size:1.1em; margin:10px 0; padding:10px; background:#ecf0f1; border-radius:4px;&quot;&gt;
                $$[CALCUL DETAILLE ETAPE PAR ETAPE]$$
            &lt;/div&gt;
        &lt;/div&gt;

        &lt;div style=&quot;background:#e8f5e8; padding:8px; border-radius:4px; margin:10px 0;&quot;&gt;
            &lt;strong&gt;✅ Solution finale :&lt;/strong&gt; [Résultat avec justification]
        &lt;/div&gt;
    &lt;/div&gt;

    &lt;h2 style=&quot;color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;&quot;&gt;V. Propriétés et caractéristiques&lt;/h2&gt;
    &lt;div style=&quot;background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;&quot;&gt;
        &lt;ul style=&quot;margin:0; padding-left:20px;&quot;&gt;
            &lt;li&gt;&lt;strong&gt;Propriété 1 :&lt;/strong&gt; [Description de la première propriété importante]&lt;/li&gt;
            &lt;li&gt;&lt;strong&gt;Propriété 2 :&lt;/strong&gt; [Description de la deuxième propriété importante]&lt;/li&gt;
            &lt;li&gt;&lt;strong&gt;Propriété 3 :&lt;/strong&gt; [Description de la troisième propriété importante]&lt;/li&gt;
            &lt;li&gt;&lt;strong&gt;Aspect graphique :&lt;/strong&gt; [Description de la représentation visuelle]&lt;/li&gt;
        &lt;/ul&gt;
    &lt;/div&gt;

    &lt;h2 style=&quot;color:#2c3e50; border-bottom:2px solid #3498db; padding-bottom:8px;&quot;&gt;VI. Erreurs fréquentes et conseils&lt;/h2&gt;
    &lt;div style=&quot;background:#ffffff; border:1px solid #e1e8ed; padding:15px; margin:15px 0; border-radius:6px;&quot;&gt;
        &lt;div style=&quot;background:#fdf2f2; padding:12px; border-radius:4px; margin-bottom:10px;&quot;&gt;
            &lt;strong&gt;❌ Pièges à éviter :&lt;/strong&gt;
            &lt;div style=&quot;margin:8px 0;&quot;&gt;
                &lt;ul style=&quot;margin:0; padding-left:20px;&quot;&gt;
                    &lt;li&gt;[Erreur fréquente 1]&lt;/li&gt;
                    &lt;li&gt;[Erreur fréquente 2]&lt;/li&gt;
                    &lt;li&gt;[Erreur fréquente 3]&lt;/li&gt;
                &lt;/ul&gt;
            &lt;/div&gt;
        &lt;/div&gt;

        &lt;div style=&quot;background:#f0f9f0; padding:12px; border-radius:4px;&quot;&gt;
            &lt;strong&gt;✅ Conseils méthodologiques :&lt;/strong&gt;
            &lt;div style=&quot;margin:8px 0;&quot;&gt;
                &lt;ul style=&quot;margin:0; padding-left:20px;&quot;&gt;
                    &lt;li&gt;[Conseil pratique 1]&lt;/li&gt;
                    &lt;li&gt;[Conseil pratique 2]&lt;/li&gt;
                    &lt;li&gt;[Conseil pratique 3]&lt;/li&gt;
                &lt;/ul&gt;
            &lt;/div&gt;
        &lt;/div&gt;
    &lt;/div&gt;

&lt;/div&gt;

===</code></pre></div><div class="format-notes" data-v-d4fcef03><p data-v-d4fcef03><strong data-v-d4fcef03>Notes importantes :</strong></p><ul data-v-d4fcef03><li data-v-d4fcef03>Utilisez <code data-v-d4fcef03>===</code> pour délimiter chaque cours</li><li data-v-d4fcef03><strong data-v-d4fcef03>⚠️ IMPORTANT :</strong> Sélectionnez d&#39;abord le chapitre dans la liste déroulante ci-dessus</li><li data-v-d4fcef03><strong data-v-d4fcef03>Chapitre :</strong> Le chapitre est automatiquement défini par votre sélection dans le dropdown</li><li data-v-d4fcef03>Difficulté : <code data-v-d4fcef03>easy</code>, <code data-v-d4fcef03>medium</code> ou <code data-v-d4fcef03>hard</code> uniquement</li><li data-v-d4fcef03>Ordre : Numéro pour l&#39;ordre d&#39;affichage (0, 1, 2, etc.)</li><li data-v-d4fcef03><strong data-v-d4fcef03>Images multiples :</strong> Séparez les noms de fichiers par des virgules : <code data-v-d4fcef03>image1.jpg,image2.png</code></li><li data-v-d4fcef03><strong data-v-d4fcef03>Positionnement d&#39;images :</strong> Utilisez <code data-v-d4fcef03>[IMAGE_1]</code>, <code data-v-d4fcef03>[IMAGE_2]</code>, etc. dans le contenu pour positionner les images</li><li data-v-d4fcef03><strong data-v-d4fcef03>Ordre des images :</strong> Les images sont assignées dans l&#39;ordre de leur déclaration (1ère = [IMAGE_1], 2ème = [IMAGE_2], etc.)</li><li data-v-d4fcef03><strong data-v-d4fcef03>Types d&#39;images automatiques :</strong> Toutes les images = &quot;Illustration&quot; par défaut</li><li data-v-d4fcef03><strong data-v-d4fcef03>Contenu :</strong> Supporte HTML et LaTeX (MathJax)</li><li data-v-d4fcef03>MathJax supporté : <code data-v-d4fcef03>$formule$</code> (inline) et <code data-v-d4fcef03>$$formule$$</code> (bloc)</li><li data-v-d4fcef03>HTML supporté : <code data-v-d4fcef03>&lt;strong&gt;gras&lt;/strong&gt;</code>, <code data-v-d4fcef03>&lt;em&gt;italique&lt;/em&gt;</code>, etc.</li><li data-v-d4fcef03>Laissez <code data-v-d4fcef03>Images:</code> vide si pas d&#39;image</li><li data-v-d4fcef03><strong data-v-d4fcef03>Champs obligatoires :</strong> Seuls <code data-v-d4fcef03>Titre:</code> et le contenu sont obligatoires</li><li data-v-d4fcef03><strong data-v-d4fcef03>Champs optionnels :</strong> <code data-v-d4fcef03>Difficulté:</code>, <code data-v-d4fcef03>Ordre:</code>, <code data-v-d4fcef03>Images:</code>, <code data-v-d4fcef03>Description:</code></li><li data-v-d4fcef03><strong data-v-d4fcef03>Template uniforme :</strong> Utilisez le template ci-dessus pour maintenir la cohérence de tous vos cours</li></ul></div></div>`,2)),a("div",mt,[M(a("input",{"onUpdate:modelValue":e[0]||(e[0]=t=>$.value=t),type:"text",placeholder:"Filtrer les chapitres...",class:"filter-input"},null,512),[[U,$.value]]),M(a("select",{"onUpdate:modelValue":e[1]||(e[1]=t=>c.value=t),required:""},[e[3]||(e[3]=a("option",{disabled:"",value:""},"Choisir chapitre",-1)),(u(!0),d(k,null,T(Y.value,t=>(u(),d("option",{key:t.id,value:t.id},g(O(t)),9,vt))),128))],512),[[ot,c.value]]),a("div",ht,[e[5]||(e[5]=a("h4",null,"📁 Images pour les cours",-1)),e[6]||(e[6]=a("p",{class:"upload-help"},"Uploadez les images qui seront référencées dans vos cours :",-1)),a("input",{type:"file",ref_key:"imagesInput",ref:L,onChange:H,accept:"image/*",multiple:"",class:"images-file-input"},null,544),b.value.length>0?(u(),d("div",xt,[e[4]||(e[4]=a("h5",null,"Images sélectionnées :",-1)),(u(!0),d(k,null,T(b.value,(t,n)=>(u(),d("div",{key:n,class:"selected-image-item"},[a("img",{src:B(t),alt:t.name,class:"image-preview"},null,8,bt),a("span",yt,g(t.name),1),a("button",{type:"button",class:"btn-remove",onClick:r=>Q(n)},"×",8,qt)]))),128))])):h("",!0)]),M(a("textarea",{"onUpdate:modelValue":e[2]||(e[2]=t=>v.value=t),placeholder:"Coller ici vos cours…",rows:"20"},null,512),[[U,v.value]]),a("div",It,[a("button",{class:"btn-secondary",onClick:X,disabled:!v.value.trim(),type:"button"},"Prévisualiser",8,Ct),a("button",{class:"btn-primary",onClick:K,disabled:!c.value||!v.value.trim()},"Créer les cours",8,Et)])]),N.value?(u(),d("div",_t,g(N.value),1)):h("",!0),m.value?(u(),d("div",$t,g(m.value),1)):h("",!0),x.value.length===0&&v.value.trim()&&w.value?(u(),d("div",At,"Aucun cours valide trouvé. Vérifiez le format.")):h("",!0),x.value.length?(u(),d("div",kt,[a("h3",null,"Aperçu ("+g(x.value.length)+")",1),(u(!0),d(k,null,T(x.value,(t,n)=>(u(),d("div",{key:n,class:"preview-item"},[a("h4",null,g(t.titre),1),t.image?(u(),d("div",Tt,[a("span",Nt,"🖼️ Images: "+g(t.image),1),a("div",Lt,[(u(!0),d(k,null,T(t.image.split(",").map(r=>r.trim()).filter(Boolean),r=>(u(),d("span",{key:r,class:S(["image-status",A(r)?"available":"missing"])},g(r)+": "+g(A(r)?"✅ Disponible":"❌ Manquante - Assurez-vous d'avoir uploadé cette image"),3))),128))])])):h("",!0),a("div",Mt,[a("div",wt,[a("span",{class:S(["difficulty-badge",t.difficulty])},g(V(t.difficulty)),3),a("span",Dt,"Ordre: "+g(t.ordre),1)]),t.description?(u(),d("div",Ot,[e[7]||(e[7]=a("strong",null,"Description:",-1)),nt(" "+g(t.description),1)])):h("",!0),a("div",{class:"preview-content",innerHTML:W(t)},null,8,Pt)])]))),128))])):h("",!0)]))}},Qt=at(Ut,[["__scopeId","data-v-d4fcef03"]]);export{Qt as default};
