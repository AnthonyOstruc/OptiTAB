from sympy import symbols, limit, oo, simplify, latex, Add, Mul, Pow, S, E, pi, log, exp, sin, cos, tan
from sympy.functions import Abs, sqrt
from sympy.parsing.latex import parse_latex
from sympy.calculus.util import continuous_domain
from sympy.core.numbers import Integer, Float
import re
import logging


logger = logging.getLogger(__name__)


class LimitCalculator:
    """Calculateur de limites avec étapes détaillées et pédagogiques"""
    
    # Constantes pour les types de limites
    LIMIT_TYPES = {
        'infinity': "limite a l'infini",
        'point': "limite en un point",
        'left': "limite a gauche",
        'right': "limite a droite",
        'indeterminate': "forme indeterminee",
        'simple': "limite directe"
    }
    
    # Formes indéterminées courantes
    INDETERMINATE_FORMS = {
        '0/0': "0/0",
        'inf/inf': "∞/∞", 
        '0*inf': "0×∞",
        'inf-inf': "∞-∞",
        '1^inf': "1^∞",
        '0^0': "0^0",
        'inf^0': "∞^0"
    }
    
    # Techniques de résolution
    RESOLUTION_TECHNIQUES = {
        'direct': "substitution directe",
        'factorization': "factorisation",
        'rationalization': "rationalisation",
        'lhopital': "regle de L'Hopital",
        'substitution': "changement de variable",
        'squeeze': "theoreme des gendarmes",
        'asymptotic': "developpement asymptotique"
    }

    def __init__(self):
        self.steps = []
        self.limit_point = None
        self.limit_direction = None

    def calculate_limit(self, expr_latex, limit_point_str=None, direction=None):
        """Calcule la limite avec étapes détaillées"""
        logger.debug(f"Traitement de l'expression: {expr_latex}; point: {limit_point_str}; direction: {direction}")
        
        # ETAPE 1: PARSING DE L'EXPRESSION ET DU POINT LIMITE
        expr, var = self._parse_expression(expr_latex)
        self.limit_point = self._parse_limit_point(limit_point_str)
        self.limit_direction = direction
        self.steps = []
        
        # ETAPE 2: IDENTIFICATION DU TYPE DE LIMITE
        self.steps.append(self._create_step(f"On calcule la limite : $\\lim_{{x \\to {self._format_limit_point()}}} {expr_latex}$"))
        limit_type = self._identify_limit_type()
        self.steps.append(self._create_step(f"Type de limite : {limit_type}"))

        # ETAPE 3: ANALYSE PRELIMINAIRE
        preliminary_analysis = self._analyze_expression(expr, var)
        self.steps.extend(preliminary_analysis)

        # ETAPE 4: APPLICATION DES TECHNIQUES DE RESOLUTION
        resolution_steps = self._apply_resolution_techniques(expr, var)
        self.steps.extend(resolution_steps)

        # ETAPE 5: CALCUL ET RESULTAT FINAL
        final_result = self._calculate_final_result(expr, var)

        logger.debug(f"Résultat final: {final_result}; étapes: {len(self.steps)}")

        return {'result_latex': final_result, 'steps': self.steps}

    def _parse_expression(self, expr_latex):
        """Parse l'expression LaTeX et identifie la variable"""
        try:
            expr = parse_latex(expr_latex)
            # Identifier la variable principale (généralement x)
            variables = list(expr.free_symbols)
            var = variables[0] if variables else symbols('x')
            logger.debug(f"Expression parsée: {expr}, Variable: {var}")
            return expr, var
        except Exception as parse_error:
            logger.error(f"Erreur parsing: {parse_error}")
            raise ValueError(f'Erreur de parsing LaTeX: {str(parse_error)}')

    def _parse_limit_point(self, limit_point_str):
        """Parse le point limite (nombre, +∞, -∞)"""
        if not limit_point_str:
            return oo  # Par défaut, limite à +∞
        
        limit_str = limit_point_str.strip().lower()
        
        if limit_str in ['+inf', '+∞', 'inf', '∞', '+infinity']:
            return oo
        elif limit_str in ['-inf', '-∞', '-infinity']:
            return -oo
        else:
            try:
                # Essayer de parser comme nombre
                if '/' in limit_str:
                    # Fraction
                    num, den = limit_str.split('/')
                    return Integer(int(num)) / Integer(int(den))
                else:
                    # Nombre entier ou décimal
                    return Float(limit_str) if '.' in limit_str else Integer(int(limit_str))
            except:
                return oo  # Par défaut

    def _format_limit_point(self):
        """Formate le point limite pour l'affichage LaTeX"""
        if self.limit_point == oo:
            return "+\\infty"
        elif self.limit_point == -oo:
            return "-\\infty"
        else:
            return latex(self.limit_point)

    def _identify_limit_type(self):
        """Identifie le type de limite"""
        if self.limit_point in [oo, -oo]:
            return self.LIMIT_TYPES['infinity']
        elif self.limit_direction == 'left':
            return self.LIMIT_TYPES['left']
        elif self.limit_direction == 'right':
            return self.LIMIT_TYPES['right']
        else:
            return self.LIMIT_TYPES['point']

    def _analyze_expression(self, expr, var):
        """Analyse preliminaire detaillee de l'expression"""
        steps = []
        
        # Verifier la continuite au point
        if self.limit_point not in [oo, -oo]:
            steps.append(self._create_step(
                "Analyse de la fonction au point limite :",
                f"On examine le comportement de $f(x) = {latex(expr)}$ quand $x \\to {self._format_limit_point()}$"
            ))
            
            try:
                value_at_point = expr.subs(var, self.limit_point)
                
                if value_at_point.is_finite and not value_at_point.has(oo, -oo) and value_at_point != S.NaN:
                    steps.append(self._create_step(
                        "Substitution directe :",
                        f"$f({latex(self.limit_point)}) = {latex(value_at_point)}$"
                    ))
                    steps.append(self._create_step(
                        "Conclusion :",
                        f"La fonction est continue en ${latex(self.limit_point)}$, donc $\\lim_{{x \\to {self._format_limit_point()}}} f(x) = {latex(value_at_point)}$"
                    ))
                    return steps
                else:
                    steps.append(self._create_step(
                        "Probleme detecte :",
                        f"La substitution directe donne une forme indeterminee ou infinie : ${latex(value_at_point)}$"
                    ))
                    steps.append(self._create_step(
                        "Methode de resolution :",
                        "Il faut utiliser des techniques avancees pour lever l'indetermination"
                    ))
            except Exception as e:
                steps.append(self._create_step(
                    "Analyse necessaire :",
                    "La fonction necessite une etude plus approfondie pour determiner la limite"
                ))
        else:
            # Analyser le comportement asymptotique
            steps.append(self._create_step(
                "Comportement asymptotique : On etudie le comportement de la fonction quand x tend vers l'infini"
            ))
            
            steps.append(self._create_step(
                "Expression a analyser :",
                f"$f(x) = {latex(expr)}$"
            ))
            
            # Identifier le terme dominant
            if isinstance(expr, Add):
                # Somme : identifier le terme dominant
                steps.append(self._create_step(
                    "Identification des termes : L'expression est une somme de plusieurs termes"
                ))
                steps.append(self._create_step(
                    "Expression complete :",
                    f"${latex(expr)}$"
                ))
                steps.append(self._create_step(
                    "Terme dominant : On identifie le terme qui croit le plus rapidement"
                ))
            elif isinstance(expr, Mul):
                # Produit : analyser les facteurs
                steps.append(self._create_step(
                    "Analyse du produit :",
                    "L'expression est un produit de plusieurs facteurs"
                ))
                steps.append(self._create_step(
                    "Expression complete :",
                    f"${latex(expr)}$"
                ))
            elif isinstance(expr, Pow):
                # Puissance : analyser base et exposant
                base, exp = expr.base, expr.exp
                steps.append(self._create_step(
                    "Analyse de la puissance :",
                    "On etudie la base et l'exposant separement"
                ))
                steps.append(self._create_step(
                    "Base et exposant :",
                    f"Base : ${latex(base)}$, Exposant : ${latex(exp)}$"
                ))
        
        return steps

    def _apply_resolution_techniques(self, expr, var):
        """Applique les techniques de résolution appropriées"""
        steps = []
        
        # Détecter les formes indéterminées
        indeterminate_form = self._detect_indeterminate_form(expr, var)
        if indeterminate_form:
            steps.append(self._create_step(f"On détecte une forme indéterminée : {indeterminate_form}"))
            steps.extend(self._handle_indeterminate_form(expr, var, indeterminate_form))
        else:
            # Limite directe
            steps.extend(self._handle_direct_limit(expr, var))
        
        return steps

    def _detect_indeterminate_form(self, expr, var):
        """Detecte les formes indeterminees"""
        try:
            # Substituer la valeur limite
            if self.limit_point == oo:
                # Pour l'infini, analyser le comportement
                if isinstance(expr, Add):
                    # Verifier ∞ - ∞
                    terms = expr.args
                    if len(terms) >= 2:
                        return self.INDETERMINATE_FORMS['inf-inf']
                elif isinstance(expr, Mul):
                    # Verifier 0 × ∞
                    return self.INDETERMINATE_FORMS['0*inf']
                elif isinstance(expr, Pow):
                    # Verifier 1^∞, 0^0, ∞^0
                    base_limit = limit(expr.base, var, self.limit_point)
                    exp_limit = limit(expr.exp, var, self.limit_point)
                    if base_limit == 1 and exp_limit == oo:
                        return self.INDETERMINATE_FORMS['1^inf']
            else:
                # Substitution directe pour detecter 0/0
                result = expr.subs(var, self.limit_point)
                if result.has(S.NaN) or str(result) == 'zoo':
                    return self.INDETERMINATE_FORMS['0/0']
        except:
            pass
        
        return None

    def _handle_indeterminate_form(self, expr, var, form):
        """Gere les formes indeterminees avec etapes detaillees"""
        steps = []
        
        steps.append(self._create_step(
            "Resolution de la forme indeterminee : Nous devons resoudre la forme indeterminee par des techniques avancees"
        ))
        
        steps.append(self._create_step(
            "Forme detectee :",
            f"${form}$"
        ))
        
        if form == self.INDETERMINATE_FORMS['0/0']:
            steps.extend(self._handle_zero_over_zero(expr, var))
        elif form == self.INDETERMINATE_FORMS['inf/inf']:
            steps.extend(self._handle_inf_over_inf(expr, var))
        elif form == self.INDETERMINATE_FORMS['0*inf']:
            steps.extend(self._handle_zero_times_inf(expr, var))
        elif form == self.INDETERMINATE_FORMS['inf-inf']:
            steps.extend(self._handle_inf_minus_inf(expr, var))
        else:
            steps.append(self._create_step(
                "Technique de resolution :",
                f"Application de methodes specialisees pour la forme ${form}$"
            ))
        
        return steps

    def _handle_zero_over_zero(self, expr, var):
        """Gere la forme indeterminee 0/0 avec details pedagogiques"""
        steps = []
        
        steps.append(self._create_step(
            "Methode 1 - Factorisation :",
            "On essaie de factoriser le numerateur et le denominateur pour simplifier"
        ))
        
        # Analyser si c'est un quotient
        if '/' in str(expr) or isinstance(expr, Mul):
            steps.append(self._create_step(
                "Identification des facteurs :",
                f"Expression : ${latex(expr)}$"
            ))
            
            steps.append(self._create_step(
                "Recherche de facteurs communs :",
                "On cherche les facteurs qui s'annulent au point limite"
            ))
        
        # Mentionner la regle de L'Hopital
        steps.append(self._create_step(
            "Methode 2 - Regle de L'Hopital :",
            "Si la factorisation ne fonctionne pas, on peut utiliser : $\\lim_{x \\to a} \\frac{f(x)}{g(x)} = \\lim_{x \\to a} \\frac{f'(x)}{g'(x)}$"
        ))
        
        return steps

    def _handle_inf_over_inf(self, expr, var):
        """Gere la forme indeterminee ∞/∞ avec analyse detaillee"""
        steps = []
        
        steps.append(self._create_step(
            "Methode - Comparaison des ordres de grandeur :",
            "Pour une forme infini sur infini, on compare les termes dominants"
        ))
        
        steps.append(self._create_step(
            "Forme mathematique :",
            "$\\frac{\\infty}{\\infty}$"
        ))
        
        steps.append(self._create_step(
            "Principe :",
            "Le terme de plus haut degre determine le comportement asymptotique"
        ))
        
        if isinstance(expr, Mul) or '/' in str(expr):
            steps.append(self._create_step(
                "Identification des termes dominants :",
                "On identifie les termes qui croissent le plus vite"
            ))
            
            steps.append(self._create_step(
                "Expression a analyser :",
                f"${latex(expr)}$"
            ))
            
            steps.append(self._create_step(
                "Simplification asymptotique :",
                "On divise numerateur et denominateur par le terme de plus haut degre"
            ))
        
        return steps

    def _handle_zero_times_inf(self, expr, var):
        """Gere la forme indeterminee 0×∞"""
        steps = []
        
        steps.append(self._create_step(
            "Transformation en quotient :",
            "Pour resoudre cette forme, on transforme en quotient"
        ))
        
        steps.append(self._create_step(
            "Formes possibles :",
            "$0 \\times \\infty = \\frac{\\infty}{\\frac{1}{0}}$ ou $\\frac{0}{\\frac{1}{\\infty}}$"
        ))
        
        steps.append(self._create_step(
            "Choix de la transformation :",
            "On choisit la forme qui nous donne une forme plus simple"
        ))
        
        steps.append(self._create_step(
            "Formes resultantes :",
            "$\\frac{0}{0}$ ou $\\frac{\\infty}{\\infty}$"
        ))
        
        return steps

    def _handle_inf_minus_inf(self, expr, var):
        """Gere la forme indeterminee ∞-∞"""
        steps = []
        
        steps.append(self._create_step(
            "Factorisation ou rationalisation : Pour resoudre cette forme, on factorise ou on rationalise l'expression"
        ))
        
        steps.append(self._create_step(
            "Forme a resoudre :",
            "$\\infty - \\infty$"
        ))
        
        if isinstance(expr, Add):
            steps.append(self._create_step(
                "Analyse des termes : On analyse chaque terme de la somme"
            ))
            
            steps.append(self._create_step(
                "Expression complete :",
                f"${latex(expr)}$"
            ))
            
            steps.append(self._create_step(
                "Factorisation du terme dominant : On factorise par le terme qui tend vers l'infini le plus rapidement"
            ))
        
        return steps

    def _handle_direct_limit(self, expr, var):
        """Gere les limites directes avec etapes detaillees"""
        steps = []
        
        if self.limit_point in [oo, -oo]:
            steps.append(self._create_step(
                "Analyse du comportement a l'infini :",
                f"On etudie $\\lim_{{x \\to {self._format_limit_point()}}} {latex(expr)}$"
            ))
            
            # Analyser le type d'expression
            if isinstance(expr, Add):
                steps.append(self._create_step(
                    "Expression de type somme :",
                    "Dans une somme, le terme dominant détermine la limite"
                ))
                
                # Identifier le terme de plus haut degré
                terms = expr.args
                steps.append(self._create_step(
                    "Identification du terme dominant :",
                    f"Parmi les termes ${', '.join([latex(term) for term in terms])}$, on identifie celui qui croît le plus vite"
                ))
                
            elif isinstance(expr, Mul):
                steps.append(self._create_step(
                    "Expression de type produit :",
                    "Dans un produit, on analyse chaque facteur séparément"
                ))
                
            elif isinstance(expr, Pow):
                base, exp = expr.base, expr.exp
                steps.append(self._create_step(
                    "Expression de type puissance :",
                    f"Pour $({latex(base)})^{{{latex(exp)}}}$, on etudie la base et l'exposant"
                ))
                # Analyser la croissance
                steps.append(self._create_step(
                    "Analyse de la croissance :",
                    f"Base : ${latex(base)} \\to$ ? et Exposant : ${latex(exp)} \\to$ ?"
                ))
            
            # Determiner le resultat
            steps.append(self._create_step(
                "Conclusion sur le comportement :",
                f"L'expression tend vers l'infini avec le meme signe que ${self._format_limit_point()}$"
            ))
            
        else:
            steps.append(self._create_step(
                "Calcul direct par substitution :",
                f"On peut calculer directement $f({latex(self.limit_point)})$"
            ))
            
            try:
                value = expr.subs(var, self.limit_point)
                steps.append(self._create_step(
                    "Substitution :",
                    f"$f({latex(self.limit_point)}) = {latex(value)}$"
                ))
            except:
                steps.append(self._create_step(
                    "Calcul nécessaire :",
                    "La substitution nécessite des calculs intermédiaires"
                ))
        
        return steps

    def _calculate_final_result(self, expr, var):
        """Calcule le resultat final avec etapes de verification"""
        try:
            # Calculer la limite avec sympy
            if self.limit_direction == 'left':
                result = limit(expr, var, self.limit_point, '-')
                direction_text = "a gauche"
            elif self.limit_direction == 'right':
                result = limit(expr, var, self.limit_point, '+')
                direction_text = "a droite"
            else:
                result = limit(expr, var, self.limit_point)
                direction_text = ""
            
            # Ajouter une etape de calcul final
            self.steps.append(self._create_step(
                "Calcul final de la limite : On applique les techniques identifiees pour obtenir le resultat"
            ))
            
            # Verifier et presenter le resultat
            if result == oo:
                self.steps.append(self._create_step(
                    "Resultat final :",
                    f"$\\lim_{{x \\to {self._format_limit_point()}}} {latex(expr)} = +\\infty$"
                ))
                return "+\\infty"
            elif result == -oo:
                self.steps.append(self._create_step(
                    "Resultat final :",
                    f"$\\lim_{{x \\to {self._format_limit_point()}}} {latex(expr)} = -\\infty$"
                ))
                return "-\\infty"
            elif result.has(S.NaN) or str(result) == 'zoo':
                self.steps.append(self._create_step(
                    "Resultat final :",
                    f"$\\lim_{{x \\to {self._format_limit_point()}}} {latex(expr)}$ n'existe pas"
                ))
                return "\\text{n'existe pas}"
            else:
                simplified_result = simplify(result)
                self.steps.append(self._create_step(
                    "Resultat final :",
                    f"$\\lim_{{x \\to {self._format_limit_point()}}} {latex(expr)} = {latex(simplified_result)}$"
                ))
                
                # Ajouter une verification si possible
                if self.limit_point not in [oo, -oo]:
                    self.steps.append(self._create_step(
                        "Verification :",
                        f"On peut verifier en calculant $f({latex(self.limit_point)}) = {latex(simplified_result)}$"
                    ))
                
                return latex(simplified_result)
                
        except Exception as e:
            logger.error(f"Erreur calcul limite: {e}")
            self.steps.append(self._create_step(
                "Erreur de calcul :",
                "Une erreur s'est produite lors du calcul de la limite"
            ))
            return "\\text{erreur}"

    def _create_step(self, text=None, formula=None):
        """Crée une étape avec texte et/ou formule"""
        step = {}
        if text:
            step['text'] = text
        if formula:
            step['formula'] = formula
        return step 