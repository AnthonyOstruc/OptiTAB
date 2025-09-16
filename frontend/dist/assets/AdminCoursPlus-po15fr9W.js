import{a as p,c as tt,B as et,b as d,a1 as at,d as n,g as b,k as D,K as U,L as it,F as k,p as T,t as g,z as ot,o as u,n as S,j as rt}from"./vendor-D171CWhe.js";import{_ as nt}from"./index-Bvm2JEkS.js";import{a as lt,g as st}from"./curriculum-Ch8J6CLY.js";import{g as dt,u as ut,c as gt,a as ct}from"./cours-CXkJGuuq.js";import{r as pt,a as mt}from"./scientificRenderer-SJJ6pUZd.js";import"./ui-jaH5oyHW.js";import"./pdf-B39ievqC.js";import"./mathlive-B5k0jhbN.js";const vt={class:"bulk-form"},ft=["value"],bt={class:"images-upload-section"},ht={key:0,class:"selected-images"},xt=["src","alt"],qt={class:"image-name"},yt=["onClick"],It={class:"btn-group"},Ct=["disabled"],Et=["disabled"],_t={key:0,class:"success-msg"},$t={key:1,class:"error-msg"},At={key:2,class:"info-msg"},kt={key:3,class:"preview-section"},Tt={key:0,class:"preview-image-info"},Lt={class:"image-indicator"},Nt={class:"image-status-list"},Dt={class:"preview-cours"},Mt={class:"preview-header"},Ot={class:"ordre-badge"},Pt={key:0,class:"preview-description"},wt=["innerHTML"],Rt=10*1024*1024,Ut={__name:"AdminCoursPlus",setup(St){const j=["image/jpeg","image/jpg","image/png","image/gif","image/webp","image/svg+xml"],y=p([]),_=p([]),$=p(""),c=p(""),f=p(""),L=p(""),v=p(""),h=p([]),M=p(!1),x=p([]),N=p(null);class z{constructor(){this.images=new Map}addImage(e){if(!this.validateImage(e))throw new Error(`Image invalide: ${e.name}`);this.images.set(e.name,e)}removeImage(e){this.images.delete(e)}validateImage(e){return!(!j.includes(e.type)||e.size>Rt)}getImage(e){return this.images.get(e)}getImageNames(){return Array.from(this.images.keys())}}const I=new z;function O(a){return _.value.find(e=>String(e.id)===String(a))}function F(a){if(!a)return null;const e=O(a.notion);if(!e)return{themeNom:"",matiereNom:"",paysNom:"",niveauNom:""};const t=e.matiere_nom||e.contexte_detail&&e.contexte_detail.matiere_nom||"",r=e.theme_nom||"",o=e.contexte_detail&&e.contexte_detail.pays?e.contexte_detail.pays.nom:"",s=e.contexte_detail&&e.contexte_detail.niveau?e.contexte_detail.niveau.nom:"";return{matiereNom:t,themeNom:r,paysNom:o,niveauNom:s}}function P(a){const e=O(a.notion),t=F(a);return[a.nom,e?`— ${e.nom}`:"",t&&t.matiereNom?`— ${t.matiereNom}`:"",t&&(t.paysNom||t.niveauNom)?`— ${[t.paysNom,t.niveauNom].filter(Boolean).join(" · ")}`:""].filter(Boolean).join(" ")}function V(a){return{easy:"Facile",medium:"Moyen",hard:"Difficile"}[a]||a}function B(a){return URL.createObjectURL(a)}function A(a){return I.getImage(a)}function W(a,e=null){return(a||"").split(",").map(r=>r.trim()).filter(Boolean).map((r,o)=>{const s=A(r);return{id:`preview-${o}`,image:s?URL.createObjectURL(s):r,image_type:"illustration",position:o+1}})}function G(a){const e=W(a.image,a);let t=a.contenu;const r=(a.image||"").split(",").map(o=>o.trim()).filter(Boolean);return t=t.replace(/\[IMAGE_(\d+)\]/g,(o,s)=>{const i=parseInt(s)-1,l=r[i],m=A(l);return m?`
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
      `}),mt(t,e)}function H(a){Array.from(a.target.files).forEach(t=>{try{I.addImage(t),x.value.push(t)}catch{}})}function Q(a){const e=x.value[a];I.removeImage(e.name),x.value.splice(a,1)}function w(a){const e=a.split("===").filter(r=>r.trim()),t=[];for(const r of e)try{const o=J(r.trim());o&&t.push(o)}catch{}return t}function J(a){const e=a.split(`
`),t={titre:"",description:"",contenu:"",difficulty:"medium",ordre:0,image:"",chapitre:c.value,matiere:null,notion:null};if(c.value){const s=y.value.find(i=>i.id==c.value);if(s){const i=_.value.find(l=>l.id==s.notion);i&&(t.notion=i.id,t.matiere=i.matiere)}}let r="header",o=[];for(let s=0;s<e.length;s++){const i=e[s].trim();i&&(r==="header"?i.startsWith("Difficulté:")?t.difficulty=i.split(":")[1].trim():i.startsWith("Ordre:")?t.ordre=parseInt(i.split(":")[1].trim())||0:i.startsWith("Chapitre:")||(i.toLowerCase().startsWith("image:")||i.toLowerCase().startsWith("images:")?t.image=i.split(":")[1].trim():i.startsWith("Titre:")?t.titre=i.split(":")[1].trim():i.startsWith("Description:")?(t.description=i.split(":")[1].trim(),r="content"):!t.titre&&!i.startsWith("===")&&(t.titre=i)):o.push(i))}return t.contenu=o.join(`
`),!t.titre||!t.contenu||!t.matiere||!t.chapitre?null:t}function X(){try{M.value=!0,h.value=w(f.value),ot(()=>{pt()})}catch{v.value="Erreur lors de la prévisualisation"}}async function K(){if(!c.value){v.value="Veuillez sélectionner un chapitre";return}const a=y.value.find(t=>t.id==c.value);if(!a){v.value="Chapitre invalide";return}if(!_.value.find(t=>t.id==a.notion)){v.value="Notion invalide pour ce chapitre";return}try{const t=w(f.value);if(t.length===0){v.value="Aucun cours valide trouvé";return}let r=0,o=0,s=0,i=null;try{const l=await dt(null,null,Number(c.value)),m=Array.isArray(l?.data)?l.data:Array.isArray(l)?l:[];m&&m.length>0&&(i=m[0].id)}catch{}for(const l of t)try{const m={chapitre:Number(l.chapitre),titre:l.titre,contenu:l.contenu,ordre:l.ordre||0,difficulty:l.difficulty||"medium"};let C;if(i)C=(await ut(i,m))?.id||i,o++;else{const{data:E}=await gt(m);C=E?.id,r++,i=C}if(l.image&&C){const E=l.image.split(",").map(q=>q.trim()).filter(Boolean);for(let q=0;q<E.length;q++){const R=I.getImage(E[q]);if(R){const Z={cours:C,image:R,image_type:"illustration",position:q+1};await ct(Z)}}}}catch{s++}if(r>0||o>0){L.value=`${r} créé(s)${o?`, ${o} mis à jour`:""}${s>0?`, ${s} erreur(s)`:""}`;const l=c.value;f.value="",h.value=[],x.value=[],I.images.clear(),N.value&&(N.value.value=""),c.value=l}else v.value="Aucun cours n'a pu être créé"}catch{v.value="Erreur lors de la création des cours"}}const Y=tt(()=>{if(!$.value)return y.value;const a=$.value.toLowerCase();return y.value.filter(e=>P(e).toLowerCase().includes(a))});return et(async()=>{try{const[a,e]=await Promise.all([lt(),st()]);y.value=Array.isArray(a)?a:a?.data||[],_.value=Array.isArray(e)?e:e?.data||[]}catch{}}),(a,e)=>(u(),d("div",null,[e[8]||(e[8]=at(`<h2 class="admin-title" data-v-3a1bc272>Bulk – Ajout de Cours</h2><div class="format-help" data-v-3a1bc272><h3 data-v-3a1bc272>📋 Format requis :</h3><div class="format-example" data-v-3a1bc272><pre data-v-3a1bc272><code data-v-3a1bc272>=== [NOM DU COURS - SOUS-TITRE]
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

===</code></pre></div><div class="format-notes" data-v-3a1bc272><p data-v-3a1bc272><strong data-v-3a1bc272>Notes importantes :</strong></p><ul data-v-3a1bc272><li data-v-3a1bc272>Utilisez <code data-v-3a1bc272>===</code> pour délimiter chaque cours</li><li data-v-3a1bc272><strong data-v-3a1bc272>⚠️ IMPORTANT :</strong> Sélectionnez d&#39;abord le chapitre dans la liste déroulante ci-dessus</li><li data-v-3a1bc272><strong data-v-3a1bc272>Chapitre :</strong> Le chapitre est automatiquement défini par votre sélection dans le dropdown</li><li data-v-3a1bc272>Difficulté : <code data-v-3a1bc272>easy</code>, <code data-v-3a1bc272>medium</code> ou <code data-v-3a1bc272>hard</code> uniquement</li><li data-v-3a1bc272>Ordre : Numéro pour l&#39;ordre d&#39;affichage (0, 1, 2, etc.)</li><li data-v-3a1bc272><strong data-v-3a1bc272>Images multiples :</strong> Séparez les noms de fichiers par des virgules : <code data-v-3a1bc272>image1.jpg,image2.png</code></li><li data-v-3a1bc272><strong data-v-3a1bc272>Positionnement d&#39;images :</strong> Utilisez <code data-v-3a1bc272>[IMAGE_1]</code>, <code data-v-3a1bc272>[IMAGE_2]</code>, etc. dans le contenu pour positionner les images</li><li data-v-3a1bc272><strong data-v-3a1bc272>Ordre des images :</strong> Les images sont assignées dans l&#39;ordre de leur déclaration (1ère = [IMAGE_1], 2ème = [IMAGE_2], etc.)</li><li data-v-3a1bc272><strong data-v-3a1bc272>Types d&#39;images automatiques :</strong> Toutes les images = &quot;Illustration&quot; par défaut</li><li data-v-3a1bc272><strong data-v-3a1bc272>Contenu :</strong> Supporte HTML et LaTeX (MathJax)</li><li data-v-3a1bc272>MathJax supporté : <code data-v-3a1bc272>$formule$</code> (inline) et <code data-v-3a1bc272>$$formule$$</code> (bloc)</li><li data-v-3a1bc272>HTML supporté : <code data-v-3a1bc272>&lt;strong&gt;gras&lt;/strong&gt;</code>, <code data-v-3a1bc272>&lt;em&gt;italique&lt;/em&gt;</code>, etc.</li><li data-v-3a1bc272>Laissez <code data-v-3a1bc272>Images:</code> vide si pas d&#39;image</li><li data-v-3a1bc272><strong data-v-3a1bc272>Champs obligatoires :</strong> Seuls <code data-v-3a1bc272>Titre:</code> et le contenu sont obligatoires</li><li data-v-3a1bc272><strong data-v-3a1bc272>Champs optionnels :</strong> <code data-v-3a1bc272>Difficulté:</code>, <code data-v-3a1bc272>Ordre:</code>, <code data-v-3a1bc272>Images:</code>, <code data-v-3a1bc272>Description:</code></li><li data-v-3a1bc272><strong data-v-3a1bc272>Template uniforme :</strong> Utilisez le template ci-dessus pour maintenir la cohérence de tous vos cours</li></ul></div></div>`,2)),n("div",vt,[D(n("input",{"onUpdate:modelValue":e[0]||(e[0]=t=>$.value=t),type:"text",placeholder:"Filtrer les chapitres...",class:"filter-input"},null,512),[[U,$.value]]),D(n("select",{"onUpdate:modelValue":e[1]||(e[1]=t=>c.value=t),required:""},[e[3]||(e[3]=n("option",{disabled:"",value:""},"Choisir chapitre",-1)),(u(!0),d(k,null,T(Y.value,t=>(u(),d("option",{key:t.id,value:t.id},g(P(t)),9,ft))),128))],512),[[it,c.value]]),n("div",bt,[e[5]||(e[5]=n("h4",null,"📁 Images pour les cours",-1)),e[6]||(e[6]=n("p",{class:"upload-help"},"Uploadez les images qui seront référencées dans vos cours :",-1)),n("input",{type:"file",ref_key:"imagesInput",ref:N,onChange:H,accept:"image/*",multiple:"",class:"images-file-input"},null,544),x.value.length>0?(u(),d("div",ht,[e[4]||(e[4]=n("h5",null,"Images sélectionnées :",-1)),(u(!0),d(k,null,T(x.value,(t,r)=>(u(),d("div",{key:r,class:"selected-image-item"},[n("img",{src:B(t),alt:t.name,class:"image-preview"},null,8,xt),n("span",qt,g(t.name),1),n("button",{type:"button",class:"btn-remove",onClick:o=>Q(r)},"×",8,yt)]))),128))])):b("",!0)]),D(n("textarea",{"onUpdate:modelValue":e[2]||(e[2]=t=>f.value=t),placeholder:"Coller ici vos cours…",rows:"20"},null,512),[[U,f.value]]),n("div",It,[n("button",{class:"btn-secondary",onClick:X,disabled:!f.value.trim(),type:"button"},"Prévisualiser",8,Ct),n("button",{class:"btn-primary",onClick:K,disabled:!c.value||!f.value.trim()},"Créer les cours",8,Et)])]),L.value?(u(),d("div",_t,g(L.value),1)):b("",!0),v.value?(u(),d("div",$t,g(v.value),1)):b("",!0),h.value.length===0&&f.value.trim()&&M.value?(u(),d("div",At,"Aucun cours valide trouvé. Vérifiez le format.")):b("",!0),h.value.length?(u(),d("div",kt,[n("h3",null,"Aperçu ("+g(h.value.length)+")",1),(u(!0),d(k,null,T(h.value,(t,r)=>(u(),d("div",{key:r,class:"preview-item"},[n("h4",null,g(t.titre),1),t.image?(u(),d("div",Tt,[n("span",Lt,"🖼️ Images: "+g(t.image),1),n("div",Nt,[(u(!0),d(k,null,T(t.image.split(",").map(o=>o.trim()).filter(Boolean),o=>(u(),d("span",{key:o,class:S(["image-status",A(o)?"available":"missing"])},g(o)+": "+g(A(o)?"✅ Disponible":"❌ Manquante - Assurez-vous d'avoir uploadé cette image"),3))),128))])])):b("",!0),n("div",Dt,[n("div",Mt,[n("span",{class:S(["difficulty-badge",t.difficulty])},g(V(t.difficulty)),3),n("span",Ot,"Ordre: "+g(t.ordre),1)]),t.description?(u(),d("div",Pt,[e[7]||(e[7]=n("strong",null,"Description:",-1)),rt(" "+g(t.description),1)])):b("",!0),n("div",{class:"preview-content",innerHTML:G(t)},null,8,wt)])]))),128))])):b("",!0)]))}},Qt=nt(Ut,[["__scopeId","data-v-3a1bc272"]]);export{Qt as default};
