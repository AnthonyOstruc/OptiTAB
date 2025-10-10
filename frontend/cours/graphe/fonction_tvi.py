import matplotlib.pyplot as plt
import numpy as np

def creer_graphique_tvi(fonction, a, b, c, titre="Théorème des Valeurs Intermédiaires", 
                       nom_fonction="f(x)", couleur_fonction='#2E8B57', 
                       couleur_points='#E74C3C', couleur_c='#F39C12'):
    """
    Crée un graphique pour illustrer le Théorème des Valeurs Intermédiaires (TVI)
    
    Paramètres:
    - fonction: fonction Python (ex: lambda x: x + 1)
    - a, b: bornes de l'intervalle [a, b]
    - c: valeur intermédiaire entre f(a) et f(b)
    - titre: titre du graphique
    - nom_fonction: nom affiché de la fonction
    - couleur_fonction: couleur de la courbe
    - couleur_points: couleur des points A et B
    - couleur_c: couleur de la valeur c et solution
    """
    
    # Configuration du style
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calcul des valeurs
    f_a = fonction(a)
    f_b = fonction(b)
    
    # Vérification que c est bien entre f(a) et f(b)
    if not (min(f_a, f_b) <= c <= max(f_a, f_b)):
        print(f"Attention: c = {c} n'est pas entre f(a) = {f_a} et f(b) = {f_b}")
    
    # Création des données
    x = np.linspace(a - 0.5, b + 0.5, 1000)
    y = fonction(x)
    
    # Tracé de la fonction
    ax.plot(x, y, color=couleur_fonction, linewidth=5, label=f'{nom_fonction}')
    
    # Points A et B
    ax.plot(a, f_a, 'o', color=couleur_points, markersize=18, markeredgewidth=4, 
            markerfacecolor='white', zorder=5)
    ax.plot(b, f_b, 'o', color=couleur_points, markersize=18, markeredgewidth=4, 
            markerfacecolor='white', zorder=5)
    
    # Ligne horizontale pour c
    ax.axhline(y=c, color=couleur_c, linestyle='--', linewidth=4, alpha=0.9)
    
    # Recherche de la solution (méthode simple)
    x_solution = None
    for i in range(len(x)-1):
        if (y[i] - c) * (y[i+1] - c) <= 0:
            # Interpolation linéaire
            x_solution = x[i] + (c - y[i]) * (x[i+1] - x[i]) / (y[i+1] - y[i])
            break
    
    if x_solution is not None:
        # Point d'intersection
        ax.plot(x_solution, c, 's', color=couleur_c, markersize=15, markeredgewidth=4, 
                markerfacecolor='white', zorder=5)
        
        # Ligne verticale pour la solution
        ax.axvline(x=x_solution, color=couleur_c, linestyle=':', linewidth=3, alpha=0.7)
    
    # Zone de l'intervalle [a, b]
    ax.axvspan(a, b, alpha=0.15, color='#3498DB')
    
    # Configuration du graphique
    marge = 0.5
    ax.set_xlim(a - marge, b + marge)
    ax.set_ylim(min(f_a, f_b, c) - 1, max(f_a, f_b, c) + 1)
    ax.grid(False)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title(titre, fontsize=20, fontweight='bold', color='#2C3E50', pad=25)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Suppression des axes
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Annotations
    ax.annotate(f'A({a}, {f_a:.1f})', xy=(a, f_a), xytext=(a-0.3, f_a+0.3),
                fontsize=14, fontweight='bold', color=couleur_points,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9))
    
    ax.annotate(f'B({b}, {f_b:.1f})', xy=(b, f_b), xytext=(b+0.1, f_b+0.3),
                fontsize=14, fontweight='bold', color=couleur_points,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9))
    
    ax.annotate(f'c = {c}', xy=(b-0.5, c), xytext=(b-0.5, c+0.4),
                fontsize=14, fontweight='bold', color=couleur_c,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9))
    
    if x_solution is not None:
        ax.annotate(f'Solution: x = {x_solution:.2f}', 
                    xy=(x_solution, c), xytext=(x_solution-0.4, c-0.4),
                    fontsize=12, fontweight='bold', color=couleur_c,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='#FEF9E7', alpha=0.9))
    
    # Texte explicatif
    ax.text((a+b)/2, max(f_a, f_b, c) + 0.5, 
            'TVI: Si f est continue sur [a, b]\net c est entre f(a) et f(b),\nalors ∃ x ∈ [a, b] tel que f(x) = c',
            fontsize=13, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#E8F4FD', alpha=0.9, 
                     edgecolor='#3498DB', linewidth=2))
    
    # Légende
    legend_elements = [
        plt.Line2D([0], [0], color=couleur_fonction, linewidth=5, label=nom_fonction),
        plt.Line2D([0], [0], marker='o', color=couleur_points, linestyle='None', 
                   markersize=12, markeredgewidth=3, markerfacecolor='white', label='Points A et B'),
        plt.Line2D([0], [0], color=couleur_c, linestyle='--', linewidth=4, label=f'Valeur c = {c}'),
    ]
    
    if x_solution is not None:
        legend_elements.append(
            plt.Line2D([0], [0], marker='s', color=couleur_c, linestyle='None', 
                      markersize=10, markeredgewidth=3, markerfacecolor='white', 
                      label=f'Solution x = {x_solution:.2f}')
        )
    
    ax.legend(handles=legend_elements, loc='upper left', fontsize=11, framealpha=0.9)
    
    # Ajustement de la mise en page
    plt.tight_layout()
    
    return fig, ax

# Exemples d'utilisation
if __name__ == "__main__":
    # Exemple 1: Fonction linéaire simple
    fig1, ax1 = creer_graphique_tvi(
        fonction=lambda x: x + 1,
        a=0, b=3, c=2.5,
        titre="TVI - Exemple 1: Fonction linéaire",
        nom_fonction="f(x) = x + 1"
    )
    plt.savefig('tvi_exemple1.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Exemple 2: Fonction quadratique
    fig2, ax2 = creer_graphique_tvi(
        fonction=lambda x: 0.5 * x**2 - 2,
        a=-2, b=2, c=-1,
        titre="TVI - Exemple 2: Fonction quadratique",
        nom_fonction="f(x) = 0.5x² - 2",
        couleur_fonction='#8E44AD'
    )
    plt.savefig('tvi_exemple2.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Exemple 3: Fonction cubique
    fig3, ax3 = creer_graphique_tvi(
        fonction=lambda x: x**3 - 3*x + 1,
        a=-2, b=2, c=0,
        titre="TVI - Exemple 3: Fonction cubique",
        nom_fonction="f(x) = x³ - 3x + 1",
        couleur_fonction='#E67E22'
    )
    plt.savefig('tvi_exemple3.png', dpi=300, bbox_inches='tight')
    plt.show()
