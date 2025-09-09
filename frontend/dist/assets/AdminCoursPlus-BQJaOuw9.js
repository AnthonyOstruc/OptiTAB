import{a as p,A as Y,b as d,P as Z,d as n,g as b,k as O,L as K,F as $,p as k,B as tt,t as u,H as et,o as g,n as w,j as at}from"./vendor-CPU10QdV.js";import{_ as it}from"./index-BhTphZWV.js";import{a as ot,g as rt}from"./curriculum-DPSaZDuo.js";import{r as nt,g as lt,u as st,c as dt,e as gt,a as ut}from"./scientificRenderer-BIHedVTI.js";import"./ui-es3YBeq-.js";import"./pdf-OEFxGcL4.js";import"./mathlive-B5k0jhbN.js";const ct={class:"bulk-form"},pt=["value"],mt={class:"images-upload-section"},vt={key:0,class:"selected-images"},ft=["src","alt"],bt={class:"image-name"},ht=["onClick"],xt={class:"btn-group"},qt=["disabled"],yt=["disabled"],It={key:0,class:"success-msg"},Ct={key:1,class:"error-msg"},Et={key:2,class:"info-msg"},_t={key:3,class:"preview-section"},At={key:0,class:"preview-image-info"},$t={class:"image-indicator"},kt={class:"image-status-list"},Tt={class:"preview-cours"},Nt={class:"preview-header"},Lt={class:"ordre-badge"},Pt={key:0,class:"preview-description"},Dt=["innerHTML"],Mt=10*1024*1024,Ot={__name:"AdminCoursPlus",setup(wt){const R=["image/jpeg","image/jpg","image/png","image/gif","image/webp","image/svg+xml"],E=p([]),_=p([]),m=p(""),f=p(""),T=p(""),v=p(""),h=p([]),L=p(!1),x=p([]),N=p(null);class U{constructor(){this.images=new Map}addImage(e){if(!this.validateImage(e))throw new Error(`Image invalide: ${e.name}`);this.images.set(e.name,e)}removeImage(e){this.images.delete(e)}validateImage(e){return!(!R.includes(e.type)||e.size>Mt)}getImage(e){return this.images.get(e)}getImageNames(){return Array.from(this.images.keys())}}const y=new U;function P(a){return _.value.find(e=>String(e.id)===String(a))}function S(a){if(!a)return null;const e=P(a.notion);if(!e)return{themeNom:"",matiereNom:"",paysNom:"",niveauNom:""};const t=e.matiere_nom||e.contexte_detail&&e.contexte_detail.matiere_nom||"",r=e.theme_nom||"",o=e.contexte_detail&&e.contexte_detail.pays?e.contexte_detail.pays.nom:"",l=e.contexte_detail&&e.contexte_detail.niveau?e.contexte_detail.niveau.nom:"";return{matiereNom:t,themeNom:r,paysNom:o,niveauNom:l}}function j(a){const e=P(a.notion),t=S(a);return[a.nom,e?`— ${e.nom}`:"",t&&t.matiereNom?`— ${t.matiereNom}`:"",t&&(t.paysNom||t.niveauNom)?`— ${[t.paysNom,t.niveauNom].filter(Boolean).join(" · ")}`:""].filter(Boolean).join(" ")}function z(a){return{easy:"Facile",medium:"Moyen",hard:"Difficile"}[a]||a}function F(a){return URL.createObjectURL(a)}function A(a){return y.getImage(a)}function B(a,e=null){return(a||"").split(",").map(r=>r.trim()).filter(Boolean).map((r,o)=>{const l=A(r);return{id:`preview-${o}`,image:l?URL.createObjectURL(l):r,image_type:"illustration",position:o+1}})}function V(a){const e=B(a.image,a);let t=a.contenu;const r=(a.image||"").split(",").map(o=>o.trim()).filter(Boolean);return t=t.replace(/\[IMAGE_(\d+)\]/g,(o,l)=>{const i=parseInt(l)-1,s=r[i],c=A(s);return c?`
        <div class="preview-image-container" style="text-align: center; margin: 2em 0;">
          <img src="${URL.createObjectURL(c)}" alt="Image ${l}" class="preview-image" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
          <div class="image-info" style="margin-top: 0.5rem; font-size: 0.875rem; color: #28a745; font-weight: 500;">✅ ${s}</div>
        </div>
      `:`
        <div class="preview-image-placeholder">
          <div class="placeholder-icon">🖼️</div>
          <div class="placeholder-text">Image manquante: ${s||`IMAGE_${l}`}</div>
          <div class="placeholder-hint">Uploadez cette image dans la section ci-dessus</div>
        </div>
      `}),ut(t,e)}function H(a){Array.from(a.target.files).forEach(t=>{try{y.addImage(t),x.value.push(t)}catch{}})}function W(a){const e=x.value[a];y.removeImage(e.name),x.value.splice(a,1)}function D(a){const e=a.split("===").filter(r=>r.trim()),t=[];for(const r of e)try{const o=G(r.trim());o&&t.push(o)}catch{}return t}function G(a){const e=a.split(`
`),t={titre:"",description:"",contenu:"",difficulty:"medium",ordre:0,image:"",chapitre:m.value,matiere:null,notion:null};if(m.value){const l=E.value.find(i=>i.id==m.value);if(l){const i=_.value.find(s=>s.id==l.notion);i&&(t.notion=i.id,t.matiere=i.matiere)}}let r="header",o=[];for(let l=0;l<e.length;l++){const i=e[l].trim();i&&(r==="header"?i.startsWith("Difficulté:")?t.difficulty=i.split(":")[1].trim():i.startsWith("Ordre:")?t.ordre=parseInt(i.split(":")[1].trim())||0:i.startsWith("Chapitre:")||(i.toLowerCase().startsWith("image:")||i.toLowerCase().startsWith("images:")?t.image=i.split(":")[1].trim():i.startsWith("Titre:")?t.titre=i.split(":")[1].trim():i.startsWith("Description:")?(t.description=i.split(":")[1].trim(),r="content"):!t.titre&&!i.startsWith("===")&&(t.titre=i)):o.push(i))}return t.contenu=o.join(`
`),!t.titre||!t.contenu||!t.matiere||!t.chapitre?null:t}function Q(){try{L.value=!0,h.value=D(f.value),et(()=>{nt()})}catch{v.value="Erreur lors de la prévisualisation"}}async function J(){if(!m.value){v.value="Veuillez sélectionner un chapitre";return}const a=E.value.find(t=>t.id==m.value);if(!a){v.value="Chapitre invalide";return}if(!_.value.find(t=>t.id==a.notion)){v.value="Notion invalide pour ce chapitre";return}try{const t=D(f.value);if(t.length===0){v.value="Aucun cours valide trouvé";return}let r=0,o=0,l=0,i=null;try{const s=await lt(null,null,Number(m.value)),c=Array.isArray(s?.data)?s.data:Array.isArray(s)?s:[];c&&c.length>0&&(i=c[0].id)}catch{}for(const s of t)try{const c={chapitre:Number(s.chapitre),titre:s.titre,contenu:s.contenu,ordre:s.ordre||0,difficulty:s.difficulty||"medium"};let I;if(i)I=(await st(i,c))?.id||i,o++;else{const{data:C}=await dt(c);I=C?.id,r++,i=I}if(s.image&&I){const C=s.image.split(",").map(q=>q.trim()).filter(Boolean);for(let q=0;q<C.length;q++){const M=y.getImage(C[q]);if(M){const X={cours:I,image:M,image_type:"illustration",position:q+1};await gt(X)}}}}catch{l++}r>0||o>0?(T.value=`${r} créé(s)${o?`, ${o} mis à jour`:""}${l>0?`, ${l} erreur(s)`:""}`,f.value="",h.value=[],x.value=[],y.images.clear(),N.value&&(N.value.value="")):v.value="Aucun cours n'a pu être créé"}catch{v.value="Erreur lors de la création des cours"}}return Y(async()=>{try{const[a,e]=await Promise.all([ot(),rt()]);E.value=Array.isArray(a)?a:a?.data||[],_.value=Array.isArray(e)?e:e?.data||[]}catch{}}),(a,e)=>(g(),d("div",null,[e[7]||(e[7]=Z(`<h2 class="admin-title" data-v-1ae6b288>Bulk – Ajout de Cours</h2><div class="format-help" data-v-1ae6b288><h3 data-v-1ae6b288>📋 Format requis :</h3><div class="format-example" data-v-1ae6b288><pre data-v-1ae6b288><code data-v-1ae6b288>=== [NOM DU COURS - SOUS-TITRE]
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

===</code></pre></div><div class="format-notes" data-v-1ae6b288><p data-v-1ae6b288><strong data-v-1ae6b288>Notes importantes :</strong></p><ul data-v-1ae6b288><li data-v-1ae6b288>Utilisez <code data-v-1ae6b288>===</code> pour délimiter chaque cours</li><li data-v-1ae6b288><strong data-v-1ae6b288>⚠️ IMPORTANT :</strong> Sélectionnez d&#39;abord le chapitre dans la liste déroulante ci-dessus</li><li data-v-1ae6b288><strong data-v-1ae6b288>Chapitre :</strong> Le chapitre est automatiquement défini par votre sélection dans le dropdown</li><li data-v-1ae6b288>Difficulté : <code data-v-1ae6b288>easy</code>, <code data-v-1ae6b288>medium</code> ou <code data-v-1ae6b288>hard</code> uniquement</li><li data-v-1ae6b288>Ordre : Numéro pour l&#39;ordre d&#39;affichage (0, 1, 2, etc.)</li><li data-v-1ae6b288><strong data-v-1ae6b288>Images multiples :</strong> Séparez les noms de fichiers par des virgules : <code data-v-1ae6b288>image1.jpg,image2.png</code></li><li data-v-1ae6b288><strong data-v-1ae6b288>Positionnement d&#39;images :</strong> Utilisez <code data-v-1ae6b288>[IMAGE_1]</code>, <code data-v-1ae6b288>[IMAGE_2]</code>, etc. dans le contenu pour positionner les images</li><li data-v-1ae6b288><strong data-v-1ae6b288>Ordre des images :</strong> Les images sont assignées dans l&#39;ordre de leur déclaration (1ère = [IMAGE_1], 2ème = [IMAGE_2], etc.)</li><li data-v-1ae6b288><strong data-v-1ae6b288>Types d&#39;images automatiques :</strong> Toutes les images = &quot;Illustration&quot; par défaut</li><li data-v-1ae6b288><strong data-v-1ae6b288>Contenu :</strong> Supporte HTML et LaTeX (MathJax)</li><li data-v-1ae6b288>MathJax supporté : <code data-v-1ae6b288>$formule$</code> (inline) et <code data-v-1ae6b288>$$formule$$</code> (bloc)</li><li data-v-1ae6b288>HTML supporté : <code data-v-1ae6b288>&lt;strong&gt;gras&lt;/strong&gt;</code>, <code data-v-1ae6b288>&lt;em&gt;italique&lt;/em&gt;</code>, etc.</li><li data-v-1ae6b288>Laissez <code data-v-1ae6b288>Images:</code> vide si pas d&#39;image</li><li data-v-1ae6b288><strong data-v-1ae6b288>Champs obligatoires :</strong> Seuls <code data-v-1ae6b288>Titre:</code> et le contenu sont obligatoires</li><li data-v-1ae6b288><strong data-v-1ae6b288>Champs optionnels :</strong> <code data-v-1ae6b288>Difficulté:</code>, <code data-v-1ae6b288>Ordre:</code>, <code data-v-1ae6b288>Images:</code>, <code data-v-1ae6b288>Description:</code></li><li data-v-1ae6b288><strong data-v-1ae6b288>Template uniforme :</strong> Utilisez le template ci-dessus pour maintenir la cohérence de tous vos cours</li></ul></div></div>`,2)),n("div",ct,[O(n("select",{"onUpdate:modelValue":e[0]||(e[0]=t=>m.value=t),required:""},[e[2]||(e[2]=n("option",{disabled:"",value:""},"Choisir chapitre",-1)),(g(!0),d($,null,k(E.value,t=>(g(),d("option",{key:t.id,value:t.id},u(j(t)),9,pt))),128))],512),[[K,m.value]]),n("div",mt,[e[4]||(e[4]=n("h4",null,"📁 Images pour les cours",-1)),e[5]||(e[5]=n("p",{class:"upload-help"},"Uploadez les images qui seront référencées dans vos cours :",-1)),n("input",{type:"file",ref_key:"imagesInput",ref:N,onChange:H,accept:"image/*",multiple:"",class:"images-file-input"},null,544),x.value.length>0?(g(),d("div",vt,[e[3]||(e[3]=n("h5",null,"Images sélectionnées :",-1)),(g(!0),d($,null,k(x.value,(t,r)=>(g(),d("div",{key:r,class:"selected-image-item"},[n("img",{src:F(t),alt:t.name,class:"image-preview"},null,8,ft),n("span",bt,u(t.name),1),n("button",{type:"button",class:"btn-remove",onClick:o=>W(r)},"×",8,ht)]))),128))])):b("",!0)]),O(n("textarea",{"onUpdate:modelValue":e[1]||(e[1]=t=>f.value=t),placeholder:"Coller ici vos cours…",rows:"20"},null,512),[[tt,f.value]]),n("div",xt,[n("button",{class:"btn-secondary",onClick:Q,disabled:!f.value.trim(),type:"button"},"Prévisualiser",8,qt),n("button",{class:"btn-primary",onClick:J,disabled:!m.value||!f.value.trim()},"Créer les cours",8,yt)])]),T.value?(g(),d("div",It,u(T.value),1)):b("",!0),v.value?(g(),d("div",Ct,u(v.value),1)):b("",!0),h.value.length===0&&f.value.trim()&&L.value?(g(),d("div",Et,"Aucun cours valide trouvé. Vérifiez le format.")):b("",!0),h.value.length?(g(),d("div",_t,[n("h3",null,"Aperçu ("+u(h.value.length)+")",1),(g(!0),d($,null,k(h.value,(t,r)=>(g(),d("div",{key:r,class:"preview-item"},[n("h4",null,u(t.titre),1),t.image?(g(),d("div",At,[n("span",$t,"🖼️ Images: "+u(t.image),1),n("div",kt,[(g(!0),d($,null,k(t.image.split(",").map(o=>o.trim()).filter(Boolean),o=>(g(),d("span",{key:o,class:w(["image-status",A(o)?"available":"missing"])},u(o)+": "+u(A(o)?"✅ Disponible":"❌ Manquante - Assurez-vous d'avoir uploadé cette image"),3))),128))])])):b("",!0),n("div",Tt,[n("div",Nt,[n("span",{class:w(["difficulty-badge",t.difficulty])},u(z(t.difficulty)),3),n("span",Lt,"Ordre: "+u(t.ordre),1)]),t.description?(g(),d("div",Pt,[e[6]||(e[6]=n("strong",null,"Description:",-1)),at(" "+u(t.description),1)])):b("",!0),n("div",{class:"preview-content",innerHTML:V(t)},null,8,Dt)])]))),128))])):b("",!0)]))}},Vt=it(Ot,[["__scopeId","data-v-1ae6b288"]]);export{Vt as default};
