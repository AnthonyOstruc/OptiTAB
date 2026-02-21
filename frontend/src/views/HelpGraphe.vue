<template>
  <MainLayout>
    <div class="help-page">
      <!-- Hero -->
      <div class="help-hero">
        <div class="help-hero-inner">
          <h1 class="help-hero-title">Guide d'utilisation — Grapheur</h1>
          <p class="help-hero-subtitle">Tout ce qu'il faut savoir pour tracer, analyser et exporter vos graphes comme un pro.</p>
          <router-link to="/calculator" class="help-back-btn">← Retour au grapheur</router-link>
        </div>
      </div>

      <!-- Table des matières -->
      <nav class="help-toc">
        <h2 class="help-toc-title">Sommaire</h2>
        <div class="help-toc-grid">
          <a href="#saisie" class="toc-card">
            <span class="toc-icon">⌨️</span>
            <span class="toc-label">Saisie rapide</span>
          </a>
          <a href="#fonctions" class="toc-card">
            <span class="toc-icon">📐</span>
            <span class="toc-label">Fonctions mathématiques</span>
          </a>
          <a href="#dessin" class="toc-card">
            <span class="toc-icon">🎨</span>
            <span class="toc-label">Outils de dessin</span>
          </a>
          <a href="#panneau" class="toc-card">
            <span class="toc-icon">📊</span>
            <span class="toc-label">Panneau latéral</span>
          </a>
          <a href="#analyse" class="toc-card">
            <span class="toc-icon">🔍</span>
            <span class="toc-label">Analyse & Calcul</span>
          </a>
          <a href="#raccourcis" class="toc-card">
            <span class="toc-icon">💡</span>
            <span class="toc-label">Astuces & raccourcis</span>
          </a>
        </div>
      </nav>

      <!-- ═══════════════════════════════ SAISIE RAPIDE ═══════════════════════════════ -->
      <section id="saisie" class="help-section">
        <div class="section-header">
          <span class="section-icon">⌨️</span>
          <h2>Saisie rapide</h2>
        </div>
        <p class="section-intro">Tapez directement dans le champ de saisie en haut du grapheur. Le système reconnaît automatiquement ce que vous voulez tracer.</p>

        <div class="example-grid">
          <!-- Courbes -->
          <div class="example-card">
            <h4>Courbes et fonctions</h4>
            <div class="example-row">
              <code>x^2</code>
              <span class="arrow">→</span>
              <span>Trace la parabole x²</span>
            </div>
            <div class="example-row">
              <code>sin(x)</code>
              <span class="arrow">→</span>
              <span>Trace la sinusoïde</span>
            </div>
            <div class="example-row">
              <code>2x^3 - 5x + 1</code>
              <span class="arrow">→</span>
              <span>Polynôme du 3e degré</span>
            </div>
            <div class="example-row">
              <code>e^(-x^2)</code>
              <span class="arrow">→</span>
              <span>Courbe en cloche (gaussienne)</span>
            </div>
            <div class="example-row">
              <code>1/x</code>
              <span class="arrow">→</span>
              <span>Hyperbole</span>
            </div>
          </div>

          <!-- Droites -->
          <div class="example-card">
            <h4>Droites</h4>
            <div class="example-row">
              <code>y = 2x + 1</code>
              <span class="arrow">→</span>
              <span>Droite de pente 2, ordonnée à l'origine 1</span>
            </div>
            <div class="example-row">
              <code>x = 3</code>
              <span class="arrow">→</span>
              <span>Droite verticale en x = 3</span>
            </div>
            <div class="example-row">
              <code>y = -2</code>
              <span class="arrow">→</span>
              <span>Droite horizontale en y = −2</span>
            </div>
            <div class="example-row">
              <code>(AB)</code>
              <span class="arrow">→</span>
              <span>Droite passant par les points A et B (s'ils existent)</span>
            </div>
          </div>

          <!-- Points -->
          <div class="example-card">
            <h4>Points</h4>
            <div class="example-row">
              <code>A(1,2)</code>
              <span class="arrow">→</span>
              <span>Crée le point A aux coordonnées (1 ; 2)</span>
            </div>
            <div class="example-row">
              <code>B(-3, 4.5)</code>
              <span class="arrow">→</span>
              <span>Point B en (−3 ; 4,5)</span>
            </div>
            <div class="example-row">
              <code>M(0,0)</code>
              <span class="arrow">→</span>
              <span>Point M à l'origine</span>
            </div>
            <p class="example-note">💡 Le nom du point est la lettre avant la parenthèse. Vous pouvez ensuite le renommer dans le panneau latéral.</p>
          </div>

          <!-- Segments & Vecteurs -->
          <div class="example-card">
            <h4>Segments, vecteurs &amp; cercles</h4>
            <div class="example-row">
              <code>[AB]</code>
              <span class="arrow">→</span>
              <span>Segment entre les points A et B</span>
            </div>
            <div class="example-row">
              <code>\vec{AB}</code>
              <span class="arrow">→</span>
              <span>Vecteur de A vers B (avec flèche)</span>
            </div>
            <div class="example-row">
              <code>C(0,0,3)</code>
              <span class="arrow">→</span>
              <span>Cercle de centre (0 ; 0) et de rayon 3</span>
            </div>
            <p class="example-note">⚠️ Les points A et B doivent exister sur le graphe avant de tracer [AB] ou \vec{AB}.</p>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════ FONCTIONS MATHÉMATIQUES ═══════════════════════════════ -->
      <section id="fonctions" class="help-section">
        <div class="section-header">
          <span class="section-icon">📐</span>
          <h2>Fonctions mathématiques supportées</h2>
        </div>
        <p class="section-intro">Vous pouvez utiliser toutes ces fonctions dans vos expressions. La notation LaTeX est aussi acceptée.</p>

        <div class="func-table-wrap">
          <table class="func-table">
            <thead>
              <tr>
                <th>Catégorie</th>
                <th>Syntaxe</th>
                <th>Description</th>
                <th>Exemple</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td rowspan="3" class="cat-cell">Trigonométrie</td>
                <td><code>sin(x)</code></td>
                <td>Sinus</td>
                <td><code>2*sin(3x)</code></td>
              </tr>
              <tr>
                <td><code>cos(x)</code></td>
                <td>Cosinus</td>
                <td><code>cos(x) + 1</code></td>
              </tr>
              <tr>
                <td><code>tan(x)</code></td>
                <td>Tangente</td>
                <td><code>tan(x/2)</code></td>
              </tr>
              <tr>
                <td rowspan="2" class="cat-cell">Logarithmes</td>
                <td><code>ln(x)</code></td>
                <td>Logarithme népérien</td>
                <td><code>ln(x+1)</code></td>
              </tr>
              <tr>
                <td><code>log(x)</code></td>
                <td>Logarithme décimal</td>
                <td><code>log(x^2)</code></td>
              </tr>
              <tr>
                <td rowspan="2" class="cat-cell">Exponentielle</td>
                <td><code>e^x</code> ou <code>exp(x)</code></td>
                <td>Exponentielle</td>
                <td><code>e^(-x^2)</code></td>
              </tr>
              <tr>
                <td><code>e^{...}</code></td>
                <td>Notation LaTeX</td>
                <td><code>e^{2x+1}</code></td>
              </tr>
              <tr>
                <td rowspan="2" class="cat-cell">Racines</td>
                <td><code>sqrt(x)</code> ou <code>\sqrt{x}</code></td>
                <td>Racine carrée</td>
                <td><code>sqrt(x+4)</code></td>
              </tr>
              <tr>
                <td><code>x^{1/3}</code></td>
                <td>Racine cubique</td>
                <td><code>x^{1/3} + 2</code></td>
              </tr>
              <tr>
                <td class="cat-cell">Valeur absolue</td>
                <td><code>|x|</code> ou <code>abs(x)</code></td>
                <td>Valeur absolue</td>
                <td><code>|x - 3| + 1</code></td>
              </tr>
              <tr>
                <td class="cat-cell">Fractions</td>
                <td><code>\frac{a}{b}</code></td>
                <td>Fraction LaTeX</td>
                <td><code>\frac{x^2 + 1}{x - 2}</code></td>
              </tr>
              <tr>
                <td class="cat-cell">Puissances</td>
                <td><code>x^n</code></td>
                <td>x à la puissance n</td>
                <td><code>x^4 - 3x^2 + 1</code></td>
              </tr>
              <tr>
                <td class="cat-cell">Constantes</td>
                <td><code>pi</code>, <code>e</code></td>
                <td>π ≈ 3.14, e ≈ 2.72</td>
                <td><code>sin(pi*x)</code></td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- ═══════════════════════════════ OUTILS DE DESSIN ═══════════════════════════════ -->
      <section id="dessin" class="help-section">
        <div class="section-header">
          <span class="section-icon">🎨</span>
          <h2>Outils de dessin</h2>
        </div>
        <p class="section-intro">La barre d'outils apparaît au-dessus du graphe. Sélectionnez un outil puis cliquez sur le graphe.</p>

        <div class="tool-cards">
          <div class="tool-card">
            <div class="tool-card-header point-bg">
              <span class="tool-emoji">🟢</span>
              <h4>Point</h4>
            </div>
            <div class="tool-card-body">
              <p><strong>1 clic</strong> sur le graphe pour placer un point.</p>
              <ul>
                <li>Le point apparaît avec un nom automatique (A, B, C…)</li>
                <li>Vous pouvez le renommer dans « Éléments tracés »</li>
                <li>Changer sa couleur via la pastille de couleur</li>
              </ul>
            </div>
          </div>

          <div class="tool-card">
            <div class="tool-card-header segment-bg">
              <span class="tool-emoji">📏</span>
              <h4>Segment</h4>
            </div>
            <div class="tool-card-body">
              <p><strong>2 clics</strong> : point de départ → point d'arrivée.</p>
              <ul>
                <li>Le 1er clic place le point de départ (marqueur temporaire)</li>
                <li>Le 2e clic place l'arrivée et trace le segment</li>
                <li>Le segment affiche son nom au milieu</li>
              </ul>
            </div>
          </div>

          <div class="tool-card">
            <div class="tool-card-header vector-bg">
              <span class="tool-emoji">➡️</span>
              <h4>Vecteur</h4>
            </div>
            <div class="tool-card-body">
              <p><strong>2 clics</strong> : origine → extrémité.</p>
              <ul>
                <li>Même principe que le segment, mais avec une flèche</li>
                <li>Le label affiche le nom du vecteur (ex: AB⃗)</li>
              </ul>
            </div>
          </div>

          <div class="tool-card">
            <div class="tool-card-header circle-bg">
              <span class="tool-emoji">⭕</span>
              <h4>Cercle</h4>
            </div>
            <div class="tool-card-body">
              <p><strong>2 clics</strong> : centre → un point du cercle.</p>
              <ul>
                <li>Le 1er clic définit le centre</li>
                <li>Le 2e clic définit le rayon (distance entre les 2 points)</li>
                <li>Le rayon s'affiche dans le label</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="help-callout info">
          <span class="callout-icon">💡</span>
          <p><strong>Important :</strong> quand un outil de dessin est actif, vous ne pouvez pas déplacer les labels ni faire de pan/zoom. Désactivez l'outil (recliquez dessus ou choisissez « Aucun ») pour retrouver ces interactions.</p>
        </div>
      </section>

      <!-- ═══════════════════════════════ PANNEAU LATÉRAL ═══════════════════════════════ -->
      <section id="panneau" class="help-section">
        <div class="section-header">
          <span class="section-icon">📊</span>
          <h2>Panneau latéral</h2>
        </div>
        <p class="section-intro">Le panneau à droite (sur bureau) ou les onglets en bas (sur mobile) vous donnent accès à toutes les options.</p>

        <div class="panel-cards">
          <div class="panel-card">
            <div class="panel-card-icon">📈</div>
            <div>
              <h4>Éléments tracés</h4>
              <p>Liste de toutes les fonctions, points, segments, vecteurs et cercles. Vous pouvez :</p>
              <ul>
                <li><strong>Renommer</strong> un élément en cliquant sur son nom</li>
                <li><strong>Changer la couleur</strong> en cliquant sur la pastille colorée</li>
                <li><strong>Supprimer</strong> un élément individuel</li>
                <li><strong>Relier les points</strong> : si vous avez ≥ 2 points, cochez « Relier les points » pour former un polygone fermé</li>
              </ul>
            </div>
          </div>

          <div class="panel-card">
            <div class="panel-card-icon">⚙️</div>
            <div>
              <h4>Axes</h4>
              <p>Configuration complète du repère :</p>
              <ul>
                <li>Afficher / masquer la grille, les axes, les graduations</li>
                <li>Personnaliser les labels des axes (ex: « temps (s) »)</li>
                <li>Définir l'intervalle (xMin, xMax, yMin, yMax)</li>
                <li><strong>Déplacer le graphique</strong> : activez cette option pour pouvoir pan + zoomer à la molette</li>
              </ul>
            </div>
          </div>

          <div class="panel-card">
            <div class="panel-card-icon">📏</div>
            <div>
              <h4>Asymptotes</h4>
              <p>Ajouter des droites de référence :</p>
              <ul>
                <li><strong>Asymptote verticale</strong> : tapez un nombre (ex: 2) → droite x = 2</li>
                <li><strong>Asymptote horizontale</strong> : tapez un nombre (ex: 0) → droite y = 0</li>
                <li>Chaque asymptote est affichée en pointillés</li>
              </ul>
            </div>
          </div>

          <div class="panel-card">
            <div class="panel-card-icon">✏️</div>
            <div>
              <h4>Formes (ajout manuel)</h4>
              <p>Ajoutez des éléments depuis le formulaire :</p>
              <ul>
                <li>Points avec coordonnées précises</li>
                <li>Segments entre 2 coordonnées</li>
                <li>Cercles avec centre et rayon</li>
                <li><strong>Textes avec LaTeX</strong> : entourez de <code>$...$</code> pour du rendu mathématique (ex: <code>$\frac{a}{b}$</code>)</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════ ANALYSE & CALCUL ═══════════════════════════════ -->
      <section id="analyse" class="help-section">
        <div class="section-header">
          <span class="section-icon">🔍</span>
          <h2>Analyse &amp; Calcul</h2>
        </div>
        <p class="section-intro">Des outils puissants pour étudier vos fonctions directement sur le graphe.</p>

        <div class="analysis-grid">
          <div class="analysis-card">
            <h4>🔀 Intersections entre courbes</h4>
            <p>Sélectionnez 2 fonctions dans le panneau « Analyse » pour trouver automatiquement leurs points d'intersection.</p>
            <div class="example-box">
              <strong>Exemple :</strong> f(x) = x² et g(x) = 2x + 3 → intersections affichées sur le graphe avec les coordonnées.
            </div>
          </div>

          <div class="analysis-card">
            <h4>📍 Racines (zéros)</h4>
            <p>Trouve les valeurs de x où f(x) = 0 (intersections avec l'axe des abscisses).</p>
            <div class="example-box">
              <strong>Exemple :</strong> f(x) = x² − 4 → racines en x = −2 et x = 2
            </div>
          </div>

          <div class="analysis-card">
            <h4>⚖️ Résolution d'inéquations</h4>
            <p>Résolvez f(x) &lt; g(x), f(x) &gt; g(x), f(x) ≤ g(x), f(x) ≥ g(x) ou f(x) = g(x).</p>
            <ul>
              <li>Choisissez 2 fonctions et un opérateur</li>
              <li>Le résultat s'affiche en notation intervalle : ex. <code>]−∞ ; 2[ ∪ ]5 ; +∞[</code></li>
              <li>La zone solution est colorée en bleu transparent sur le graphe</li>
            </ul>
            <div class="example-box">
              <strong>Exemple :</strong> f(x) = x² et g(x) = 4 avec l'opérateur « &lt; » → résultat : <code>]−2 ; 2[</code>
            </div>
          </div>

          <div class="analysis-card">
            <h4>📐 Tangente</h4>
            <p>Trace la droite tangente à une courbe en un point donné.</p>
            <div class="example-box">
              <strong>Exemple :</strong> Tangente à f(x) = x² en x = 1 → droite y = 2x − 1
            </div>
          </div>

          <div class="analysis-card">
            <h4>∫ Aire sous la courbe</h4>
            <p>Calcule l'intégrale (aire) entre une courbe et l'axe des x sur un intervalle [a, b].</p>
            <div class="example-box">
              <strong>Exemple :</strong> Aire sous x² entre 0 et 2 → zone colorée + valeur affichée
            </div>
          </div>

          <div class="analysis-card">
            <h4>∫ Aire entre 2 courbes</h4>
            <p>Calcule l'aire entre deux fonctions sur un intervalle. La zone est colorée sur le graphe.</p>
            <div class="example-box">
              <strong>Exemple :</strong> Aire entre f(x) = x et g(x) = x² sur [0, 1]
            </div>
          </div>
        </div>
      </section>

      <!-- ═══════════════════════════════ ASTUCES & RACCOURCIS ═══════════════════════════════ -->
      <section id="raccourcis" class="help-section">
        <div class="section-header">
          <span class="section-icon">💡</span>
          <h2>Astuces &amp; raccourcis</h2>
        </div>

        <div class="tips-grid">
          <div class="tip-card">
            <div class="tip-icon">🏷️</div>
            <h4>Labels déplaçables</h4>
            <p>Cliquez et glissez les labels des courbes, points, segments et cercles directement sur le graphe pour les repositionner. Cela ne fonctionne que quand <strong>aucun outil de dessin n'est actif</strong>.</p>
          </div>

          <div class="tip-card">
            <div class="tip-icon">🔗</div>
            <h4>Relier les points</h4>
            <p>Créez plusieurs points, puis cochez « Relier les points » dans le panneau « Éléments tracés ». Tous les points seront connectés en un <strong>polygone fermé</strong> (le dernier se relie au premier).</p>
          </div>

          <div class="tip-card">
            <div class="tip-icon">🔍</div>
            <h4>Zoom &amp; déplacement</h4>
            <p>Utilisez les boutons 🔍+ / 🔍− pour zoomer. Pour pouvoir <strong>déplacer le graphe</strong> (pan) et zoomer à la <strong>molette</strong>, activez l'option « Déplacer le graphique » dans l'onglet Axes.</p>
          </div>

          <div class="tip-card">
            <div class="tip-icon">📷</div>
            <h4>Export haute résolution</h4>
            <p>Cliquez sur l'icône 📷 en haut à droite du graphe pour télécharger une <strong>image PNG haute résolution</strong> (5x). L'image garde exactement le même cadrage que votre écran.</p>
          </div>

          <div class="tip-card">
            <div class="tip-icon">🗑️</div>
            <h4>Effacer tout</h4>
            <p>Le bouton rouge « Effacer tout » supprime toutes les courbes, points, segments, vecteurs, cercles et annotations en un clic.</p>
          </div>

          <div class="tip-card">
            <div class="tip-icon">🎨</div>
            <h4>Personnalisation des couleurs</h4>
            <p>Chaque élément tracé a sa propre couleur. Cliquez sur la pastille dans « Éléments tracés » pour changer la couleur d'un point, segment, vecteur ou cercle.</p>
          </div>

          <div class="tip-card">
            <div class="tip-icon">📝</div>
            <h4>Textes LaTeX</h4>
            <p>Dans l'onglet Formes, ajoutez des annotations texte. Utilisez <code>$...$</code> pour du rendu LaTeX. Exemples : <code>$\frac{1}{2}$</code>, <code>$\vec{AB}$</code>, <code>$\int_0^1 x\,dx$</code>.</p>
          </div>

          <div class="tip-card">
            <div class="tip-icon">🧮</div>
            <h4>Saisie intelligente</h4>
            <p>Le champ de saisie accepte aussi bien la notation classique (<code>sqrt(x)</code>) que LaTeX (<code>\sqrt{x}</code>). La conversion est automatique.</p>
          </div>
        </div>
      </section>

      <!-- CTA retour -->
      <div class="help-cta">
        <router-link to="/calculator" class="help-cta-btn">
          📈 Ouvrir le grapheur
        </router-link>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import MainLayout from '@/components/layout/MainLayout.vue'
</script>

<style scoped>
/* ═══════════════════════ GLOBAL ═══════════════════════ */
.help-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 20px 60px;
  color: #1e293b;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ═══════════════════════ HERO ═══════════════════════ */
.help-hero {
  text-align: center;
  padding: 60px 20px 40px;
}
.help-hero-title {
  font-size: 2.2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 12px;
}
.help-hero-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  max-width: 600px;
  margin: 0 auto 20px;
}
.help-back-btn {
  display: inline-block;
  color: #3b82f6;
  font-weight: 600;
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.2s;
}
.help-back-btn:hover {
  color: #2563eb;
}

/* ═══════════════════════ TOC ═══════════════════════ */
.help-toc {
  margin-bottom: 50px;
}
.help-toc-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #334155;
}
.help-toc-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 12px;
}
.toc-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  text-decoration: none;
  color: #334155;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s;
}
.toc-card:hover {
  background: #eff6ff;
  border-color: #93c5fd;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}
.toc-icon {
  font-size: 1.4rem;
}

/* ═══════════════════════ SECTIONS ═══════════════════════ */
.help-section {
  margin-bottom: 56px;
  scroll-margin-top: 80px;
}
.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}
.section-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}
.section-icon {
  font-size: 1.8rem;
}
.section-intro {
  color: #64748b;
  font-size: 1rem;
  margin-bottom: 24px;
  line-height: 1.6;
}

/* ═══════════════════════ EXAMPLE CARDS (SAISIE) ═══════════════════════ */
.example-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}
.example-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.example-card h4 {
  font-size: 1rem;
  font-weight: 700;
  color: #334155;
  margin: 0 0 14px;
  padding-bottom: 10px;
  border-bottom: 2px solid #eff6ff;
}
.example-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
  font-size: 0.92rem;
}
.example-row code {
  background: #f1f5f9;
  padding: 3px 8px;
  border-radius: 6px;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.85rem;
  color: #7c3aed;
  font-weight: 600;
  white-space: nowrap;
}
.arrow {
  color: #94a3b8;
  font-weight: 600;
}
.example-note {
  margin-top: 12px;
  font-size: 0.85rem;
  color: #64748b;
  background: #fffbeb;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #fde68a;
}

/* ═══════════════════════ FUNC TABLE ═══════════════════════ */
.func-table-wrap {
  overflow-x: auto;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.func-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.92rem;
}
.func-table thead {
  background: #f8fafc;
}
.func-table th {
  text-align: left;
  padding: 12px 16px;
  font-weight: 700;
  color: #334155;
  border-bottom: 2px solid #e2e8f0;
}
.func-table td {
  padding: 10px 16px;
  border-bottom: 1px solid #f1f5f9;
  color: #475569;
}
.func-table code {
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 5px;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.85rem;
  color: #7c3aed;
  font-weight: 600;
}
.cat-cell {
  font-weight: 700;
  color: #334155;
  background: #f8fafc;
}

/* ═══════════════════════ TOOL CARDS (DESSIN) ═══════════════════════ */
.tool-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}
.tool-card {
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  background: #fff;
}
.tool-card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  color: #fff;
  font-weight: 700;
}
.tool-card-header h4 {
  margin: 0;
  font-size: 1rem;
}
.tool-emoji {
  font-size: 1.5rem;
}
.point-bg { background: linear-gradient(135deg, #22c55e, #16a34a); }
.segment-bg { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.vector-bg { background: linear-gradient(135deg, #f59e0b, #d97706); }
.circle-bg { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }

.tool-card-body {
  padding: 16px 18px;
}
.tool-card-body p {
  margin: 0 0 10px;
  font-size: 0.92rem;
  color: #475569;
}
.tool-card-body ul {
  margin: 0;
  padding-left: 18px;
  font-size: 0.88rem;
  color: #64748b;
}
.tool-card-body li {
  margin-bottom: 4px;
}

/* ═══════════════════════ CALLOUT ═══════════════════════ */
.help-callout {
  display: flex;
  gap: 12px;
  padding: 16px 20px;
  border-radius: 12px;
  font-size: 0.92rem;
  line-height: 1.6;
}
.help-callout.info {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  color: #1e40af;
}
.callout-icon {
  font-size: 1.3rem;
  flex-shrink: 0;
}

/* ═══════════════════════ PANEL CARDS ═══════════════════════ */
.panel-cards {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.panel-card {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.panel-card-icon {
  font-size: 2rem;
  flex-shrink: 0;
}
.panel-card h4 {
  margin: 0 0 6px;
  font-size: 1rem;
  font-weight: 700;
  color: #334155;
}
.panel-card p {
  margin: 0 0 8px;
  font-size: 0.92rem;
  color: #475569;
  line-height: 1.5;
}
.panel-card ul {
  margin: 0;
  padding-left: 18px;
  font-size: 0.88rem;
  color: #64748b;
}
.panel-card li {
  margin-bottom: 4px;
}
.panel-card code {
  background: #f1f5f9;
  padding: 1px 5px;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #7c3aed;
}

/* ═══════════════════════ ANALYSIS GRID ═══════════════════════ */
.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}
.analysis-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.analysis-card h4 {
  margin: 0 0 10px;
  font-size: 1rem;
  font-weight: 700;
  color: #334155;
}
.analysis-card p {
  margin: 0 0 10px;
  font-size: 0.92rem;
  color: #475569;
  line-height: 1.5;
}
.analysis-card ul {
  margin: 0 0 12px;
  padding-left: 18px;
  font-size: 0.88rem;
  color: #64748b;
}
.analysis-card li {
  margin-bottom: 4px;
}
.analysis-card code {
  background: #f1f5f9;
  padding: 1px 5px;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #7c3aed;
}
.example-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 12px 14px;
  font-size: 0.88rem;
  color: #475569;
}
.example-box strong {
  color: #334155;
}

/* ═══════════════════════ TIPS GRID ═══════════════════════ */
.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}
.tip-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  transition: transform 0.2s, box-shadow 0.2s;
}
.tip-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}
.tip-icon {
  font-size: 2rem;
  margin-bottom: 10px;
}
.tip-card h4 {
  margin: 0 0 8px;
  font-size: 0.95rem;
  font-weight: 700;
  color: #334155;
}
.tip-card p {
  margin: 0;
  font-size: 0.88rem;
  color: #64748b;
  line-height: 1.5;
}
.tip-card code {
  background: #f1f5f9;
  padding: 1px 5px;
  border-radius: 4px;
  font-size: 0.82rem;
  color: #7c3aed;
}

/* ═══════════════════════ CTA ═══════════════════════ */
.help-cta {
  text-align: center;
  margin-top: 40px;
}
.help-cta-btn {
  display: inline-block;
  padding: 14px 36px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: #fff;
  font-weight: 700;
  font-size: 1.05rem;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.2s;
  box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3);
}
.help-cta-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

/* ═══════════════════════ RESPONSIVE ═══════════════════════ */
@media (max-width: 768px) {
  .help-hero-title {
    font-size: 1.6rem;
  }
  .help-hero-subtitle {
    font-size: 0.95rem;
  }
  .help-toc-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .section-header h2 {
    font-size: 1.25rem;
  }
  .example-grid,
  .tool-cards,
  .analysis-grid,
  .tips-grid {
    grid-template-columns: 1fr;
  }
  .panel-card {
    flex-direction: column;
    gap: 10px;
  }
  .func-table th,
  .func-table td {
    padding: 8px 10px;
    font-size: 0.82rem;
  }
}

@media (max-width: 480px) {
  .help-page {
    padding: 0 12px 40px;
  }
  .help-hero {
    padding: 40px 10px 24px;
  }
  .help-toc-grid {
    grid-template-columns: 1fr;
  }
}
</style>
