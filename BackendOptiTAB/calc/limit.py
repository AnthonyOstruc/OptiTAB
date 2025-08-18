from sympy import symbols, limit, oo, simplify, latex, Add, Mul, Pow, S, E, pi, log, exp, sin, cos, tan
from sympy.functions import Abs, sqrt
from sympy.parsing.latex import parse_latex
from sympy.calculus.util import continuous_domain
from sympy.core.numbers import Integer, Float
import re


class LimitCalculator:
    """Calculateur de limites avec étapes détaillées et pédagogiques"""
    
    # Constantes pour les types de limites
    LIMIT_TYPES = {
        'infinity': "limite à l'infini",
        'point': "limite en un point",
        'left': "limite à gauche",
        'right': "limite à droite",
        'indeterminate': "forme indéterminée",
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
        'lhopital': "règle de L'Hôpital",
        'substitution': "changement de variable",
        'squeeze': "théorème des gendarmes",
        'asymptotic': "développement asymptotique"
    }

    def __init__(self):
        self.steps = []
        self.limit_point = None
        self.limit_direction = None

    def calculate_limit(self, expr_latex, limit_point_str=None, direction=None):
        """Calcule la limite avec étapes détaillées"""
        print(f"Traitement de l'expression: {expr_latex}")
        print(f"Point limite: {limit_point_str}, Direction: {direction}")
        
        # ÉTAPE 1: PARSING DE L'EXPRESSION ET DU POINT LIMITE
        expr, var = self._parse_expression(expr_latex)
        self.limit_point = self._parse_limit_point(limit_point_str)
        self.limit_direction = direction
        self.steps = []
        
        # ÉTAPE 2: IDENTIFICATION DU TYPE DE LIMITE
        self.steps.append(self._create_step(f"On calcule la limite : $\\lim_{{x \\to {self._format_limit_point()}}} {expr_latex}$"))
        limit_type = self._identify_limit_type()
        self.steps.append(self._create_step(f"Type de limite : {limit_type}"))

        # ÉTAPE 3: ANALYSE PRÉLIMINAIRE
        preliminary_analysis = self._analyze_expression(expr, var)
        self.steps.extend(preliminary_analysis)

        # ÉTAPE 4: APPLICATION DES TECHNIQUES DE RÉSOLUTION
        resolution_steps = self._apply_resolution_techniques(expr, var)
        self.steps.extend(resolution_steps)

        # ÉTAPE 5: CALCUL ET RÉSULTAT FINAL
        final_result = self._calculate_final_result(expr, var)

        print(f"Résultat final: {final_result}")
        print(f"Nombre d'étapes: {len(self.steps)}")

        return {'result_latex': final_result, 'steps': self.steps}

    def _parse_expression(self, expr_latex):
        """Parse l'expression LaTeX et identifie la variable"""
        try:
            expr = parse_latex(expr_latex)
            # Identifier la variable principale (généralement x)
            variables = list(expr.free_symbols)
            var = variables[0] if variables else symbols('x')
            print(f"Expression parsée: {expr}, Variable: {var}")
            return expr, var
        except Exception as parse_error:
            print(f"Erreur parsing: {parse_error}")
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
        """Analyse préliminaire de l'expression"""
        steps = []
        
        # Vérifier la continuité au point
        if self.limit_point not in [oo, -oo]:
            try:
                value_at_point = expr.subs(var, self.limit_point)
                if value_at_point.is_finite and not value_at_point.has(oo, -oo):
                    steps.append(self._create_step(
                        f"On vérifie la valeur en ${latex(self.limit_point)}$ : $f({latex(self.limit_point)}) = {latex(value_at_point)}$"
                    ))
                    if value_at_point != S.NaN:
                        steps.append(self._create_step(
                            "La fonction est continue en ce point, donc la limite existe et vaut la valeur de la fonction"
                        ))
                        return steps
                else:
                    steps.append(self._create_step(
                        "La fonction n'est pas définie en ce point, il faut utiliser d'autres techniques"
                    ))
            except:
                steps.append(self._create_step(
                    "Analyse de la continuité nécessaire"
                ))
        
        # Analyser le comportement asymptotique
        if self.limit_point in [oo, -oo]:
            steps.append(self._create_step(
                "Pour une limite à l'infini, on analyse le comportement asymptotique"
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
        """Détecte les formes indéterminées"""
        try:
            # Substituer la valeur limite
            if self.limit_point == oo:
                # Pour l'infini, analyser le comportement
                if isinstance(expr, Add):
                    # Vérifier ∞ - ∞
                    terms = expr.args
                    if len(terms) >= 2:
                        return self.INDETERMINATE_FORMS['inf-inf']
                elif isinstance(expr, Mul):
                    # Vérifier 0 × ∞
                    return self.INDETERMINATE_FORMS['0*inf']
                elif isinstance(expr, Pow):
                    # Vérifier 1^∞, 0^0, ∞^0
                    base_limit = limit(expr.base, var, self.limit_point)
                    exp_limit = limit(expr.exp, var, self.limit_point)
                    if base_limit == 1 and exp_limit == oo:
                        return self.INDETERMINATE_FORMS['1^inf']
            else:
                # Substitution directe pour détecter 0/0
                result = expr.subs(var, self.limit_point)
                if result.has(S.NaN) or str(result) == 'zoo':
                    return self.INDETERMINATE_FORMS['0/0']
        except:
            pass
        
        return None

    def _handle_indeterminate_form(self, expr, var, form):
        """Gère les formes indéterminées"""
        steps = []
        
        if form == self.INDETERMINATE_FORMS['0/0']:
            steps.extend(self._handle_zero_over_zero(expr, var))
        elif form == self.INDETERMINATE_FORMS['inf/inf']:
            steps.extend(self._handle_inf_over_inf(expr, var))
        elif form == self.INDETERMINATE_FORMS['0*inf']:
            steps.extend(self._handle_zero_times_inf(expr, var))
        else:
            steps.append(self._create_step(
                f"Résolution de la forme indéterminée {form} par techniques avancées"
            ))
        
        return steps

    def _handle_zero_over_zero(self, expr, var):
        """Gère la forme indéterminée 0/0"""
        steps = []
        
        # Essayer la factorisation
        if isinstance(expr, Mul) and len(expr.args) == 2:
            # Cas d'un quotient
            numerator = expr.args[0] if expr.args[1].is_negative else expr.args[0]
            denominator = expr.args[1] if expr.args[1].is_negative else expr.args[1]
            
            steps.append(self._create_step(
                "On essaie de factoriser le numérateur et le dénominateur"
            ))
            
            # Utiliser la règle de L'Hôpital si nécessaire
            steps.append(self._create_step(
                "On peut appliquer la règle de L'Hôpital : $\\lim_{x \\to a} \\frac{f(x)}{g(x)} = \\lim_{x \\to a} \\frac{f'(x)}{g'(x)}$"
            ))
        
        return steps

    def _handle_inf_over_inf(self, expr, var):
        """Gère la forme indéterminée ∞/∞"""
        steps = []
        
        steps.append(self._create_step(
            "Pour une forme ∞/∞, on compare les ordres de grandeur"
        ))
        
        if isinstance(expr, Mul):
            # Analyser les termes dominants
            steps.append(self._create_step(
                "On identifie les termes de plus haut degré au numérateur et au dénominateur"
            ))
        
        return steps

    def _handle_zero_times_inf(self, expr, var):
        """Gère la forme indéterminée 0×∞"""
        steps = []
        
        steps.append(self._create_step(
            "Pour une forme 0×∞, on transforme en quotient"
        ))
        
        return steps

    def _handle_direct_limit(self, expr, var):
        """Gère les limites directes (pas de forme indéterminée)"""
        steps = []
        
        if self.limit_point in [oo, -oo]:
            steps.append(self._create_step(
                "On détermine le terme dominant pour le comportement à l'infini"
            ))
        else:
            steps.append(self._create_step(
                "On peut calculer la limite par substitution directe"
            ))
        
        return steps

    def _calculate_final_result(self, expr, var):
        """Calcule le résultat final de la limite"""
        try:
            # Calculer la limite avec sympy
            if self.limit_direction == 'left':
                result = limit(expr, var, self.limit_point, '-')
            elif self.limit_direction == 'right':
                result = limit(expr, var, self.limit_point, '+')
            else:
                result = limit(expr, var, self.limit_point)
            
            # Vérifier si le résultat est fini
            if result == oo:
                self.steps.append(self._create_step("La limite est $+\\infty$"))
                return "+\\infty"
            elif result == -oo:
                self.steps.append(self._create_step("La limite est $-\\infty$"))
                return "-\\infty"
            elif result.has(S.NaN):
                self.steps.append(self._create_step("La limite n'existe pas"))
                return "\\text{n'existe pas}"
            else:
                simplified_result = simplify(result)
                self.steps.append(self._create_step(
                    f"La limite vaut : ${latex(simplified_result)}$"
                ))
                return latex(simplified_result)
                
        except Exception as e:
            print(f"Erreur calcul limite: {e}")
            self.steps.append(self._create_step("Erreur dans le calcul de la limite"))
            return "\\text{erreur}"

    def _create_step(self, text=None, formula=None):
        """Crée une étape avec texte et/ou formule"""
        step = {}
        if text:
            step['text'] = text
        if formula:
            step['formula'] = formula
        return step 