import{a as p,c as tt,e as et,b as d,a1 as it,d as a,i as b,m as M,K as U,M as ot,F as k,s as T,t as g,B as rt,o as u,n as S,l as nt}from"./vendor-1gmgAmFu.js";import{_ as at}from"./index-DdsjLnq7.js";import{a as lt,f as st}from"./curriculum-6-VMzQHc.js";import{g as dt,u as ut,c as gt,a as ct}from"./cours-CxVEuYUx.js";import{r as pt,a as mt}from"./scientificRenderer-SJJ6pUZd.js";import"./ui-jaH5oyHW.js";import"./pdf-B39ievqC.js";import"./mathlive-B5k0jhbN.js";const vt={class:"bulk-form"},ft=["value"],bt={class:"images-upload-section"},ht={key:0,class:"selected-images"},xt=["src","alt"],qt={class:"image-name"},yt=["onClick"],It={class:"btn-group"},Ct=["disabled"],Et=["disabled"],_t={key:0,class:"success-msg"},$t={key:1,class:"error-msg"},At={key:2,class:"info-msg"},kt={key:3,class:"preview-section"},Tt={key:0,class:"preview-image-info"},Lt={class:"image-indicator"},Nt={class:"image-status-list"},Mt={class:"preview-cours"},Dt={class:"preview-header"},Ot={class:"ordre-badge"},Pt={key:0,class:"preview-description"},wt=["innerHTML"],Rt=10*1024*1024,Ut={__name:"AdminCoursPlus",setup(St){const j=["image/jpeg","image/jpg","image/png","image/gif","image/webp","image/svg+xml"],y=p([]),_=p([]),$=p(""),c=p(""),f=p(""),L=p(""),v=p(""),h=p([]),D=p(!1),x=p([]),N=p(null);class z{constructor(){this.images=new Map}addImage(e){if(!this.validateImage(e))throw new Error(`Image invalide: ${e.name}`);this.images.set(e.name,e)}removeImage(e){this.images.delete(e)}validateImage(e){return!(!j.includes(e.type)||e.size>Rt)}getImage(e){return this.images.get(e)}getImageNames(){return Array.from(this.images.keys())}}const I=new z;function O(i){return _.value.find(e=>String(e.id)===String(i))}function F(i){if(!i)return null;const e=O(i.notion);if(!e)return{themeNom:"",matiereNom:"",paysNom:"",niveauNom:""};const t=e.matiere_nom||e.contexte_detail&&e.contexte_detail.matiere_nom||"",n=e.theme_nom||"",r=e.contexte_detail&&e.contexte_detail.pays?e.contexte_detail.pays.nom:"",s=e.contexte_detail&&e.contexte_detail.niveau?e.contexte_detail.niveau.nom:"";return{matiereNom:t,themeNom:n,paysNom:r,niveauNom:s}}function P(i){const e=O(i.notion),t=F(i);return[i.nom,e?`— ${e.nom}`:"",t&&t.matiereNom?`— ${t.matiereNom}`:"",t&&(t.paysNom||t.niveauNom)?`— ${[t.paysNom,t.niveauNom].filter(Boolean).join(" · ")}`:""].filter(Boolean).join(" ")}function V(i){return{easy:"Facile",medium:"Moyen",hard:"Difficile"}[i]||i}function B(i){return URL.createObjectURL(i)}function A(i){return I.getImage(i)}function W(i,e=null){return(i||"").split(",").map(n=>n.trim()).filter(Boolean).map((n,r)=>{const s=A(n);return{id:`preview-${r}`,image:s?URL.createObjectURL(s):n,image_type:"illustration",position:r+1}})}function G(i){const e=W(i.image,i);let t=i.contenu;const n=(i.image||"").split(",").map(r=>r.trim()).filter(Boolean);return t=t.replace(/\[IMAGE_(\d+)\]/g,(r,s)=>{const o=parseInt(s)-1,l=n[o],m=A(l);return m?`
        <div class="preview-image-container" style="text-align: center; margin: 2em 0;">
          <img src="${URL.createObjectURL(m)}" alt="Image ${s}" class="preview-image" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
          <div class="image-info" style="margin-top: 0.5rem; font-size: 0.875rem; color: #28a745; font-weight: 500;">✅ ${l}</div>
        </div>
      `:`
        <div class="preview-image-placeholder">
          <div class="placeholder-icon">🖼️</div>
          <div class="placeholder-text">Image manquante: ${l||`IMAGE_${s}`}</div>
          <div class="placeholder-hint">Uploadez cette image dans la section ci-dessus</div>
        </div>
      `}),mt(t,e)}function H(i){Array.from(i.target.files).forEach(t=>{try{I.addImage(t),x.value.push(t)}catch{}})}function Q(i){const e=x.value[i];I.removeImage(e.name),x.value.splice(i,1)}function w(i){const e=i.split("===").filter(n=>n.trim()),t=[];for(const n of e)try{const r=J(n.trim());r&&t.push(r)}catch{}return t}function J(i){const e=i.split(`
`),t={titre:"",description:"",contenu:"",difficulty:"medium",ordre:0,image:"",chapitre:c.value,matiere:null,notion:null};if(c.value){const s=y.value.find(o=>o.id==c.value);if(s){const o=_.value.find(l=>l.id==s.notion);o&&(t.notion=o.id,t.matiere=o.matiere)}}let n="header",r=[];for(let s=0;s<e.length;s++){const o=e[s].trim();o&&(n==="header"?o.startsWith("Difficulté:")?t.difficulty=o.split(":")[1].trim():o.startsWith("Ordre:")?t.ordre=parseInt(o.split(":")[1].trim())||0:o.startsWith("Chapitre:")||(o.toLowerCase().startsWith("image:")||o.toLowerCase().startsWith("images:")?t.image=o.split(":")[1].trim():o.startsWith("Titre:")?t.titre=o.split(":")[1].trim():o.startsWith("Description:")?(t.description=o.split(":")[1].trim(),n="content"):!t.titre&&!o.startsWith("===")&&(t.titre=o)):r.push(o))}return t.contenu=r.join(`
`),!t.titre||!t.contenu||!t.matiere||!t.chapitre?null:t}function X(){try{D.value=!0,h.value=w(f.value),rt(()=>{pt()})}catch{v.value="Erreur lors de la prévisualisation"}}async function K(){if(!c.value){v.value="Veuillez sélectionner un chapitre";return}const i=y.value.find(t=>t.id==c.value);if(!i){v.value="Chapitre invalide";return}if(!_.value.find(t=>t.id==i.notion)){v.value="Notion invalide pour ce chapitre";return}try{const t=w(f.value);if(t.length===0){v.value="Aucun cours valide trouvé";return}let n=0,r=0,s=0,o=null;try{const l=await dt(null,null,Number(c.value)),m=Array.isArray(l?.data)?l.data:Array.isArray(l)?l:[];m&&m.length>0&&(o=m[0].id)}catch{}for(const l of t)try{const m={chapitre:Number(l.chapitre),titre:l.titre,contenu:l.contenu,ordre:l.ordre||0,difficulty:l.difficulty||"medium"};let C;if(o)C=(await ut(o,m))?.id||o,r++;else{const{data:E}=await gt(m);C=E?.id,n++,o=C}if(l.image&&C){const E=l.image.split(",").map(q=>q.trim()).filter(Boolean);for(let q=0;q<E.length;q++){const R=I.getImage(E[q]);if(R){const Z={cours:C,image:R,image_type:"illustration",position:q+1};await ct(Z)}}}}catch{s++}if(n>0||r>0){L.value=`${n} créé(s)${r?`, ${r} mis à jour`:""}${s>0?`, ${s} erreur(s)`:""}`;const l=c.value;f.value="",h.value=[],x.value=[],I.images.clear(),N.value&&(N.value.value=""),c.value=l}else v.value="Aucun cours n'a pu être créé"}catch{v.value="Erreur lors de la création des cours"}}const Y=tt(()=>{if(!$.value)return y.value;const i=$.value.toLowerCase();return y.value.filter(e=>P(e).toLowerCase().includes(i))});return et(async()=>{try{const[i,e]=await Promise.all([lt(),st()]);y.value=Array.isArray(i)?i:i?.data||[],_.value=Array.isArray(e)?e:e?.data||[]}catch{}}),(i,e)=>(u(),d("div",null,[e[8]||(e[8]=it(`<h2 class="admin-title" data-v-67dc108b>Bulk – Ajout de Cours</h2><div class="format-help" data-v-67dc108b><h3 data-v-67dc108b>📋 Format requis :</h3><div class="format-example" data-v-67dc108b><pre data-v-67dc108b><code data-v-67dc108b>=== [NOM DU COURS - SOUS-TITRE]
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

===</code></pre></div><div class="format-notes" data-v-67dc108b><p data-v-67dc108b><strong data-v-67dc108b>Notes importantes :</strong></p><ul data-v-67dc108b><li data-v-67dc108b>Utilisez <code data-v-67dc108b>===</code> pour délimiter chaque cours</li><li data-v-67dc108b><strong data-v-67dc108b>⚠️ IMPORTANT :</strong> Sélectionnez d&#39;abord le chapitre dans la liste déroulante ci-dessus</li><li data-v-67dc108b><strong data-v-67dc108b>Chapitre :</strong> Le chapitre est automatiquement défini par votre sélection dans le dropdown</li><li data-v-67dc108b>Difficulté : <code data-v-67dc108b>easy</code>, <code data-v-67dc108b>medium</code> ou <code data-v-67dc108b>hard</code> uniquement</li><li data-v-67dc108b>Ordre : Numéro pour l&#39;ordre d&#39;affichage (0, 1, 2, etc.)</li><li data-v-67dc108b><strong data-v-67dc108b>Images multiples :</strong> Séparez les noms de fichiers par des virgules : <code data-v-67dc108b>image1.jpg,image2.png</code></li><li data-v-67dc108b><strong data-v-67dc108b>Positionnement d&#39;images :</strong> Utilisez <code data-v-67dc108b>[IMAGE_1]</code>, <code data-v-67dc108b>[IMAGE_2]</code>, etc. dans le contenu pour positionner les images</li><li data-v-67dc108b><strong data-v-67dc108b>Ordre des images :</strong> Les images sont assignées dans l&#39;ordre de leur déclaration (1ère = [IMAGE_1], 2ème = [IMAGE_2], etc.)</li><li data-v-67dc108b><strong data-v-67dc108b>Types d&#39;images automatiques :</strong> Toutes les images = &quot;Illustration&quot; par défaut</li><li data-v-67dc108b><strong data-v-67dc108b>Contenu :</strong> Supporte HTML et LaTeX (MathJax)</li><li data-v-67dc108b>MathJax supporté : <code data-v-67dc108b>$formule$</code> (inline) et <code data-v-67dc108b>$$formule$$</code> (bloc)</li><li data-v-67dc108b>HTML supporté : <code data-v-67dc108b>&lt;strong&gt;gras&lt;/strong&gt;</code>, <code data-v-67dc108b>&lt;em&gt;italique&lt;/em&gt;</code>, etc.</li><li data-v-67dc108b>Laissez <code data-v-67dc108b>Images:</code> vide si pas d&#39;image</li><li data-v-67dc108b><strong data-v-67dc108b>Champs obligatoires :</strong> Seuls <code data-v-67dc108b>Titre:</code> et le contenu sont obligatoires</li><li data-v-67dc108b><strong data-v-67dc108b>Champs optionnels :</strong> <code data-v-67dc108b>Difficulté:</code>, <code data-v-67dc108b>Ordre:</code>, <code data-v-67dc108b>Images:</code>, <code data-v-67dc108b>Description:</code></li><li data-v-67dc108b><strong data-v-67dc108b>Template uniforme :</strong> Utilisez le template ci-dessus pour maintenir la cohérence de tous vos cours</li></ul></div></div>`,2)),a("div",vt,[M(a("input",{"onUpdate:modelValue":e[0]||(e[0]=t=>$.value=t),type:"text",placeholder:"Filtrer les chapitres...",class:"filter-input"},null,512),[[U,$.value]]),M(a("select",{"onUpdate:modelValue":e[1]||(e[1]=t=>c.value=t),required:""},[e[3]||(e[3]=a("option",{disabled:"",value:""},"Choisir chapitre",-1)),(u(!0),d(k,null,T(Y.value,t=>(u(),d("option",{key:t.id,value:t.id},g(P(t)),9,ft))),128))],512),[[ot,c.value]]),a("div",bt,[e[5]||(e[5]=a("h4",null,"📁 Images pour les cours",-1)),e[6]||(e[6]=a("p",{class:"upload-help"},"Uploadez les images qui seront référencées dans vos cours :",-1)),a("input",{type:"file",ref_key:"imagesInput",ref:N,onChange:H,accept:"image/*",multiple:"",class:"images-file-input"},null,544),x.value.length>0?(u(),d("div",ht,[e[4]||(e[4]=a("h5",null,"Images sélectionnées :",-1)),(u(!0),d(k,null,T(x.value,(t,n)=>(u(),d("div",{key:n,class:"selected-image-item"},[a("img",{src:B(t),alt:t.name,class:"image-preview"},null,8,xt),a("span",qt,g(t.name),1),a("button",{type:"button",class:"btn-remove",onClick:r=>Q(n)},"×",8,yt)]))),128))])):b("",!0)]),M(a("textarea",{"onUpdate:modelValue":e[2]||(e[2]=t=>f.value=t),placeholder:"Coller ici vos cours…",rows:"20"},null,512),[[U,f.value]]),a("div",It,[a("button",{class:"btn-secondary",onClick:X,disabled:!f.value.trim(),type:"button"},"Prévisualiser",8,Ct),a("button",{class:"btn-primary",onClick:K,disabled:!c.value||!f.value.trim()},"Créer les cours",8,Et)])]),L.value?(u(),d("div",_t,g(L.value),1)):b("",!0),v.value?(u(),d("div",$t,g(v.value),1)):b("",!0),h.value.length===0&&f.value.trim()&&D.value?(u(),d("div",At,"Aucun cours valide trouvé. Vérifiez le format.")):b("",!0),h.value.length?(u(),d("div",kt,[a("h3",null,"Aperçu ("+g(h.value.length)+")",1),(u(!0),d(k,null,T(h.value,(t,n)=>(u(),d("div",{key:n,class:"preview-item"},[a("h4",null,g(t.titre),1),t.image?(u(),d("div",Tt,[a("span",Lt,"🖼️ Images: "+g(t.image),1),a("div",Nt,[(u(!0),d(k,null,T(t.image.split(",").map(r=>r.trim()).filter(Boolean),r=>(u(),d("span",{key:r,class:S(["image-status",A(r)?"available":"missing"])},g(r)+": "+g(A(r)?"✅ Disponible":"❌ Manquante - Assurez-vous d'avoir uploadé cette image"),3))),128))])])):b("",!0),a("div",Mt,[a("div",Dt,[a("span",{class:S(["difficulty-badge",t.difficulty])},g(V(t.difficulty)),3),a("span",Ot,"Ordre: "+g(t.ordre),1)]),t.description?(u(),d("div",Pt,[e[7]||(e[7]=a("strong",null,"Description:",-1)),nt(" "+g(t.description),1)])):b("",!0),a("div",{class:"preview-content",innerHTML:G(t)},null,8,wt)])]))),128))])):b("",!0)]))}},Qt=at(Ut,[["__scopeId","data-v-67dc108b"]]);export{Qt as default};
