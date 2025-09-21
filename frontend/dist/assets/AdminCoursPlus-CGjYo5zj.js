import{a as p,c as tt,e as et,b as d,ap as at,d as n,i as h,m as w,K as U,N as it,F as k,s as T,t as g,B as ot,o as u,n as S,l as rt}from"./vendor-D06lVl9u.js";import{_ as nt}from"./index-0Yj6yYCO.js";import{a as lt,f as st}from"./curriculum-DVrh_iRh.js";import{g as dt,u as ut,c as gt,a as ct}from"./cours-DVzgM8zm.js";import{r as pt,a as mt}from"./scientificRenderer-V0r-XcBv.js";import"./ui-jaH5oyHW.js";import"./pdf-S6SQ1w6P.js";import"./mathlive-B5k0jhbN.js";const ft={class:"bulk-form"},vt=["value"],ht={class:"images-upload-section"},xt={key:0,class:"selected-images"},bt=["src","alt"],yt={class:"image-name"},qt=["onClick"],It={class:"btn-group"},Ct=["disabled"],Et=["disabled"],_t={key:0,class:"success-msg"},$t={key:1,class:"error-msg"},At={key:2,class:"info-msg"},kt={key:3,class:"preview-section"},Tt={key:0,class:"preview-image-info"},Nt={class:"image-indicator"},Lt={class:"image-status-list"},wt={class:"preview-cours"},Mt={class:"preview-header"},Dt={class:"ordre-badge"},Ot={key:0,class:"preview-description"},Pt=["innerHTML"],Rt=10*1024*1024,Ut={__name:"AdminCoursPlus",setup(St){const j=["image/jpeg","image/jpg","image/png","image/gif","image/webp","image/svg+xml"],q=p([]),_=p([]),$=p(""),c=p(""),v=p(""),N=p(""),f=p(""),x=p([]),M=p(!1),b=p([]),L=p(null);class z{constructor(){this.images=new Map}addImage(e){if(!this.validateImage(e))throw new Error(`Image invalide: ${e.name}`);this.images.set(e.name,e)}removeImage(e){this.images.delete(e)}validateImage(e){return!(!j.includes(e.type)||e.size>Rt)}getImage(e){return this.images.get(e)}getImageNames(){return Array.from(this.images.keys())}}const I=new z;function D(a){return _.value.find(e=>String(e.id)===String(a))}function F(a){if(!a)return null;const e=D(a.notion);if(!e)return{themeNom:"",matiereNom:"",paysNom:"",niveauNom:""};const t=e.matiere_nom||e.contexte_detail&&e.contexte_detail.matiere_nom||"",r=e.theme_nom||"",o=e.contexte_detail&&e.contexte_detail.pays?e.contexte_detail.pays.nom:"",l=e.contexte_detail&&e.contexte_detail.niveau?e.contexte_detail.niveau.nom:"";return{matiereNom:t,themeNom:r,paysNom:o,niveauNom:l}}function O(a){const e=D(a.notion),t=F(a);return[a.nom,e?`— ${e.nom}`:"",t&&t.matiereNom?`— ${t.matiereNom}`:"",t&&(t.paysNom||t.niveauNom)?`— ${[t.paysNom,t.niveauNom].filter(Boolean).join(" · ")}`:""].filter(Boolean).join(" ")}function V(a){return{easy:"Facile",medium:"Moyen",hard:"Difficile"}[a]||a}function B(a){return URL.createObjectURL(a)}function A(a){return I.getImage(a)}function G(a,e=null){return(a||"").split(",").map(r=>r.trim()).filter(Boolean).map((r,o)=>{const l=A(r);return{id:`preview-${o}`,image:l?URL.createObjectURL(l):r,image_type:"illustration",position:o+1}})}function W(a){const e=G(a.image,a);let t=a.contenu;const r=(a.image||"").split(",").map(o=>o.trim()).filter(Boolean);if(t=t.replace(/\[IMAGE_(\d+)\]/g,(o,l)=>{const i=parseInt(l)-1,s=r[i],m=A(s);return m?`
        <div class="preview-image-container" style="text-align: center; margin: 2em 0;">
          <img src="${URL.createObjectURL(m)}" alt="Image ${l}" class="preview-image" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
          <div class="image-info" style="margin-top: 0.5rem; font-size: 0.875rem; color: #28a745; font-weight: 500;">✅ ${s}</div>
        </div>
      `:`
        <div class="preview-image-placeholder">
          <div class="placeholder-icon">🖼️</div>
          <div class="placeholder-text">Image manquante: ${s||`IMAGE_${l}`}</div>
          <div class="placeholder-hint">Uploadez cette image dans la section ci-dessus</div>
        </div>
      `}),!/\[IMAGE_\d+\]/.test(a.contenu||"")&&e.length>0){const o=e.map(l=>`
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
${o}`}return mt(t,e)}function H(a){Array.from(a.target.files).forEach(t=>{try{I.addImage(t),b.value.push(t)}catch{}})}function Q(a){const e=b.value[a];I.removeImage(e.name),b.value.splice(a,1)}function P(a){const e=a.split("===").filter(r=>r.trim()),t=[];for(const r of e)try{const o=J(r.trim());o&&t.push(o)}catch{}return t}function J(a){const e=a.split(`
`),t={titre:"",description:"",contenu:"",difficulty:"medium",ordre:0,image:"",chapitre:c.value,matiere:null,notion:null};if(c.value){const l=q.value.find(i=>i.id==c.value);if(l){const i=_.value.find(s=>s.id==l.notion);i&&(t.notion=i.id,t.matiere=i.matiere)}}let r="header",o=[];for(let l=0;l<e.length;l++){const i=e[l].trim();i&&(r==="header"?i.startsWith("Difficulté:")?t.difficulty=i.split(":")[1].trim():i.startsWith("Ordre:")?t.ordre=parseInt(i.split(":")[1].trim())||0:i.startsWith("Chapitre:")||(i.toLowerCase().startsWith("image:")||i.toLowerCase().startsWith("images:")?t.image=i.split(":")[1].trim():i.startsWith("Titre:")?t.titre=i.split(":")[1].trim():i.startsWith("Description:")?(t.description=i.split(":")[1].trim(),r="content"):!t.titre&&!i.startsWith("===")&&(t.titre=i)):o.push(i))}return t.contenu=o.join(`
`),!t.titre||!t.contenu||!t.matiere||!t.chapitre?null:t}function X(){try{M.value=!0,x.value=P(v.value),ot(()=>{pt()})}catch{f.value="Erreur lors de la prévisualisation"}}async function K(){if(!c.value){f.value="Veuillez sélectionner un chapitre";return}const a=q.value.find(t=>t.id==c.value);if(!a){f.value="Chapitre invalide";return}if(!_.value.find(t=>t.id==a.notion)){f.value="Notion invalide pour ce chapitre";return}try{const t=P(v.value);if(t.length===0){f.value="Aucun cours valide trouvé";return}let r=0,o=0,l=0,i=null;try{const s=await dt(null,null,Number(c.value)),m=Array.isArray(s?.data)?s.data:Array.isArray(s)?s:[];m&&m.length>0&&(i=m[0].id)}catch{}for(const s of t)try{const m={chapitre:Number(s.chapitre),titre:s.titre,contenu:s.contenu,ordre:s.ordre||0,difficulty:s.difficulty||"medium"};let C;if(i)C=(await ut(i,m))?.id||i,o++;else{const{data:E}=await gt(m);C=E?.id,r++,i=C}if(s.image&&C){const E=s.image.split(",").map(y=>y.trim()).filter(Boolean);for(let y=0;y<E.length;y++){const R=I.getImage(E[y]);if(R){const Z={cours:C,image:R,image_type:"illustration",position:y+1};await ct(Z)}}}}catch{l++}if(r>0||o>0){N.value=`${r} créé(s)${o?`, ${o} mis à jour`:""}${l>0?`, ${l} erreur(s)`:""}`;const s=c.value;v.value="",x.value=[],b.value=[],I.images.clear(),L.value&&(L.value.value=""),c.value=s}else f.value="Aucun cours n'a pu être créé"}catch{f.value="Erreur lors de la création des cours"}}const Y=tt(()=>{if(!$.value)return q.value;const a=$.value.toLowerCase();return q.value.filter(e=>O(e).toLowerCase().includes(a))});return et(async()=>{try{const[a,e]=await Promise.all([lt(),st()]);q.value=Array.isArray(a)?a:a?.data||[],_.value=Array.isArray(e)?e:e?.data||[]}catch{}}),(a,e)=>(u(),d("div",null,[e[8]||(e[8]=at(`<h2 class="admin-title" data-v-0a1f837d>Bulk – Ajout de Cours</h2><div class="format-help" data-v-0a1f837d><h3 data-v-0a1f837d>📋 Format requis :</h3><div class="format-example" data-v-0a1f837d><pre data-v-0a1f837d><code data-v-0a1f837d>=== [NOM DU COURS - SOUS-TITRE]
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

===</code></pre></div><div class="format-notes" data-v-0a1f837d><p data-v-0a1f837d><strong data-v-0a1f837d>Notes importantes :</strong></p><ul data-v-0a1f837d><li data-v-0a1f837d>Utilisez <code data-v-0a1f837d>===</code> pour délimiter chaque cours</li><li data-v-0a1f837d><strong data-v-0a1f837d>⚠️ IMPORTANT :</strong> Sélectionnez d&#39;abord le chapitre dans la liste déroulante ci-dessus</li><li data-v-0a1f837d><strong data-v-0a1f837d>Chapitre :</strong> Le chapitre est automatiquement défini par votre sélection dans le dropdown</li><li data-v-0a1f837d>Difficulté : <code data-v-0a1f837d>easy</code>, <code data-v-0a1f837d>medium</code> ou <code data-v-0a1f837d>hard</code> uniquement</li><li data-v-0a1f837d>Ordre : Numéro pour l&#39;ordre d&#39;affichage (0, 1, 2, etc.)</li><li data-v-0a1f837d><strong data-v-0a1f837d>Images multiples :</strong> Séparez les noms de fichiers par des virgules : <code data-v-0a1f837d>image1.jpg,image2.png</code></li><li data-v-0a1f837d><strong data-v-0a1f837d>Positionnement d&#39;images :</strong> Utilisez <code data-v-0a1f837d>[IMAGE_1]</code>, <code data-v-0a1f837d>[IMAGE_2]</code>, etc. dans le contenu pour positionner les images</li><li data-v-0a1f837d><strong data-v-0a1f837d>Ordre des images :</strong> Les images sont assignées dans l&#39;ordre de leur déclaration (1ère = [IMAGE_1], 2ème = [IMAGE_2], etc.)</li><li data-v-0a1f837d><strong data-v-0a1f837d>Types d&#39;images automatiques :</strong> Toutes les images = &quot;Illustration&quot; par défaut</li><li data-v-0a1f837d><strong data-v-0a1f837d>Contenu :</strong> Supporte HTML et LaTeX (MathJax)</li><li data-v-0a1f837d>MathJax supporté : <code data-v-0a1f837d>$formule$</code> (inline) et <code data-v-0a1f837d>$$formule$$</code> (bloc)</li><li data-v-0a1f837d>HTML supporté : <code data-v-0a1f837d>&lt;strong&gt;gras&lt;/strong&gt;</code>, <code data-v-0a1f837d>&lt;em&gt;italique&lt;/em&gt;</code>, etc.</li><li data-v-0a1f837d>Laissez <code data-v-0a1f837d>Images:</code> vide si pas d&#39;image</li><li data-v-0a1f837d><strong data-v-0a1f837d>Champs obligatoires :</strong> Seuls <code data-v-0a1f837d>Titre:</code> et le contenu sont obligatoires</li><li data-v-0a1f837d><strong data-v-0a1f837d>Champs optionnels :</strong> <code data-v-0a1f837d>Difficulté:</code>, <code data-v-0a1f837d>Ordre:</code>, <code data-v-0a1f837d>Images:</code>, <code data-v-0a1f837d>Description:</code></li><li data-v-0a1f837d><strong data-v-0a1f837d>Template uniforme :</strong> Utilisez le template ci-dessus pour maintenir la cohérence de tous vos cours</li></ul></div></div>`,2)),n("div",ft,[w(n("input",{"onUpdate:modelValue":e[0]||(e[0]=t=>$.value=t),type:"text",placeholder:"Filtrer les chapitres...",class:"filter-input"},null,512),[[U,$.value]]),w(n("select",{"onUpdate:modelValue":e[1]||(e[1]=t=>c.value=t),required:""},[e[3]||(e[3]=n("option",{disabled:"",value:""},"Choisir chapitre",-1)),(u(!0),d(k,null,T(Y.value,t=>(u(),d("option",{key:t.id,value:t.id},g(O(t)),9,vt))),128))],512),[[it,c.value]]),n("div",ht,[e[5]||(e[5]=n("h4",null,"📁 Images pour les cours",-1)),e[6]||(e[6]=n("p",{class:"upload-help"},"Uploadez les images qui seront référencées dans vos cours :",-1)),n("input",{type:"file",ref_key:"imagesInput",ref:L,onChange:H,accept:"image/*",multiple:"",class:"images-file-input"},null,544),b.value.length>0?(u(),d("div",xt,[e[4]||(e[4]=n("h5",null,"Images sélectionnées :",-1)),(u(!0),d(k,null,T(b.value,(t,r)=>(u(),d("div",{key:r,class:"selected-image-item"},[n("img",{src:B(t),alt:t.name,class:"image-preview"},null,8,bt),n("span",yt,g(t.name),1),n("button",{type:"button",class:"btn-remove",onClick:o=>Q(r)},"×",8,qt)]))),128))])):h("",!0)]),w(n("textarea",{"onUpdate:modelValue":e[2]||(e[2]=t=>v.value=t),placeholder:"Coller ici vos cours…",rows:"20"},null,512),[[U,v.value]]),n("div",It,[n("button",{class:"btn-secondary",onClick:X,disabled:!v.value.trim(),type:"button"},"Prévisualiser",8,Ct),n("button",{class:"btn-primary",onClick:K,disabled:!c.value||!v.value.trim()},"Créer les cours",8,Et)])]),N.value?(u(),d("div",_t,g(N.value),1)):h("",!0),f.value?(u(),d("div",$t,g(f.value),1)):h("",!0),x.value.length===0&&v.value.trim()&&M.value?(u(),d("div",At,"Aucun cours valide trouvé. Vérifiez le format.")):h("",!0),x.value.length?(u(),d("div",kt,[n("h3",null,"Aperçu ("+g(x.value.length)+")",1),(u(!0),d(k,null,T(x.value,(t,r)=>(u(),d("div",{key:r,class:"preview-item"},[n("h4",null,g(t.titre),1),t.image?(u(),d("div",Tt,[n("span",Nt,"🖼️ Images: "+g(t.image),1),n("div",Lt,[(u(!0),d(k,null,T(t.image.split(",").map(o=>o.trim()).filter(Boolean),o=>(u(),d("span",{key:o,class:S(["image-status",A(o)?"available":"missing"])},g(o)+": "+g(A(o)?"✅ Disponible":"❌ Manquante - Assurez-vous d'avoir uploadé cette image"),3))),128))])])):h("",!0),n("div",wt,[n("div",Mt,[n("span",{class:S(["difficulty-badge",t.difficulty])},g(V(t.difficulty)),3),n("span",Dt,"Ordre: "+g(t.ordre),1)]),t.description?(u(),d("div",Ot,[e[7]||(e[7]=n("strong",null,"Description:",-1)),rt(" "+g(t.description),1)])):h("",!0),n("div",{class:"preview-content",innerHTML:W(t)},null,8,Pt)])]))),128))])):h("",!0)]))}},Qt=nt(Ut,[["__scopeId","data-v-0a1f837d"]]);export{Qt as default};
