from sympy import symbols, diff, simplify, latex, Add, Mul, Pow, S, E, expand, factor, integrate, oo
from sympy.functions import sin, cos, tan, exp, log, sqrt
from sympy.parsing.latex import parse_latex
import logging


logger = logging.getLogger(__name__)


class IntegralCalculator:
    """Calculateur d'intégrales avec étapes détaillées et pédagogiques"""
    
    # Constantes pour les types d'intégrales
    INTEGRAL_TYPES = {
        'indefinite': "intégrale indéfinie",
        'definite': "intégrale définie"
    }
    
    # Constantes pour les types de fonctions
    FUNCTION_TYPES = {
        'polynomial': "fonction polynomiale",
        'rational': "fonction rationnelle",
        'trigonometric': "fonction trigonométrique",
        'exponential': "fonction exponentielle",
        'logarithmic': "fonction logarithmique",
        'composite': "fonction composée",
        'constant': "constante"
    }
    
    # Constantes pour les méthodes d'intégration
    INTEGRATION_METHODS = {
        'direct': "intégration directe",
        'substitution': "changement de variable",
        'parts': "intégration par parties",
        'partial_fractions': "décomposition en fractions partielles"
    }
    
    # Constantes pour les formules d'intégration
    INTEGRATION_FORMULAS = {
        'power': "$\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$ (pour $n \\neq -1$)",
        'constant': "$\\int k dx = kx + C$",
        'sum': "$\\int (f(x) + g(x)) dx = \\int f(x) dx + \\int g(x) dx$",
        'sin': "$\\int \\sin(x) dx = -\\cos(x) + C$",
        'cos': "$\\int \\cos(x) dx = \\sin(x) + C$",
        'exp': "$\\int e^x dx = e^x + C$",
        'log': "$\\int \\frac{1}{x} dx = \\ln|x| + C$"
    }

    def __init__(self):
        self.steps = []

    def calculate_integral(self, expr_latex, lower_bound=None, upper_bound=None):
        """Calcule l'intégrale avec étapes détaillées et pédagogiques"""
        logger.debug(f"Traitement de l'intégrale: {expr_latex}")
        
        self.steps = []
        
        # ÉTAPE 1: IDENTIFIER LE TYPE D'INTÉGRALE
        integral_type = self._identify_integral_type(expr_latex, lower_bound, upper_bound)
        
        # ÉTAPE 2: PARSING ET ANALYSE DE L'INTÉGRANDE
        expr, var = self._parse_and_analyze_integrand(expr_latex)
        
        # ÉTAPE 3: SIMPLIFICATION DE LA FONCTION
        expr, expr_latex = self._simplify_function(expr, expr_latex)
        
        # ÉTAPE 4: SÉLECTION DE LA MÉTHODE D'INTÉGRATION
        method = self._select_integration_method(expr)
        
        # ÉTAPE 5: CALCUL DE LA PRIMITIVE
        primitive = self._compute_antiderivative(expr, var, method)
        
        # ÉTAPE 6 & 7: CALCUL FINAL ET SIMPLIFICATION
        result = self._calculate_final_result(primitive, var, lower_bound, upper_bound, integral_type)
        
        logger.debug(f"Résultat final: {result}; étapes: {len(self.steps)}")

        return {'result_latex': result, 'steps': self.steps}

    def _identify_integral_type(self, expr_latex, lower_bound, upper_bound):
        """ÉTAPE 1: Identifie le type d'intégrale (définie ou indéfinie)"""
        if lower_bound is not None and upper_bound is not None:
            integral_type = self.INTEGRAL_TYPES['definite']
            self.steps.append(self._create_step(
                f"On calcule l'intégrale définie :",
                f"$\\int_{{{lower_bound}}}^{{{upper_bound}}} {expr_latex} dx$"
            ))
            self.steps.append(self._create_step(
                f"Type d'intégrale identifié : {integral_type} avec bornes [{lower_bound}, {upper_bound}]"
            ))
        else:
            integral_type = self.INTEGRAL_TYPES['indefinite']
            self.steps.append(self._create_step(
                f"On calcule l'intégrale indéfinie :",
                f"$\\int {expr_latex} dx$"
            ))
            self.steps.append(self._create_step(
                f"Type d'intégrale identifié : {integral_type}"
            ))
        
        return integral_type

    def _parse_and_analyze_integrand(self, expr_latex):
        """ÉTAPE 2: Parse et analyse la fonction à intégrer"""
        try:
            expr = parse_latex(expr_latex)
            expr = expr.subs(symbols('e'), E)
            var = list(expr.free_symbols)[0] if expr.free_symbols else symbols('x')
            logger.debug(f"Fonction parsée: {expr}")
        except Exception as parse_error:
            logger.error(f"Erreur parsing: {parse_error}")
            raise ValueError(f'Erreur de parsing LaTeX: {str(parse_error)}')
        
        # Analyse de la structure de la fonction à intégrer
        function_type = self._analyze_function_structure(expr)
        self.steps.append(self._create_step(
            f"Analyse de la fonction à intégrer :",
            f"${expr_latex}$"
        ))
        self.steps.append(self._create_step(
            f"Type de fonction identifié : {function_type}"
        ))
        
        return expr, var

    def _analyze_function_structure(self, expr):
        """Analyse la structure de la fonction à intégrer"""
        if expr.is_Number:
            return self.FUNCTION_TYPES['constant']
        elif isinstance(expr, Add):
            return self.FUNCTION_TYPES['polynomial']
        elif isinstance(expr, Pow) and expr.exp.is_Number:
            return self.FUNCTION_TYPES['polynomial']
        elif self.is_quotient(expr):
            return self.FUNCTION_TYPES['rational']
        elif hasattr(expr, 'func') and expr.func.__name__ in ['sin', 'cos', 'tan']:
            return self.FUNCTION_TYPES['trigonometric']
        elif hasattr(expr, 'func') and expr.func.__name__ == 'exp':
            return self.FUNCTION_TYPES['exponential']
        elif hasattr(expr, 'func') and expr.func.__name__ == 'log':
            return self.FUNCTION_TYPES['logarithmic']
        elif isinstance(expr, Mul) and len(expr.args) > 1:
            return self.FUNCTION_TYPES['composite']
        else:
            return self.FUNCTION_TYPES['polynomial']

    def _simplify_function(self, expr, expr_latex):
        """ÉTAPE 3: Simplifie la fonction à intégrer si possible"""
        expr_original = expr
        expr_simplified = simplify(expr)
        
        if expr != expr_simplified:
            self.steps.append(self._create_step(
                "Simplification de la fonction :", 
                f"{latex(expr)} = {latex(expr_simplified)}"
            ))
            expr = expr_simplified
            expr_latex = latex(expr)
        else:
            self.steps.append(self._create_step(
                "Simplification de la fonction :", 
                f"{latex(expr)} = {latex(expr_simplified)}"
            ))
        
        return expr, expr_latex

    def _select_integration_method(self, expr):
        """ÉTAPE 4: Sélectionne la méthode d'intégration appropriée"""
        if expr.is_Number:
            method = self.INTEGRATION_METHODS['direct']
            self.steps.append(self._create_step(
                f"Méthode sélectionnée : {method} - intégration d'une constante"
            ))
        elif isinstance(expr, Add):
            method = self.INTEGRATION_METHODS['direct']
            self.steps.append(self._create_step(
                f"Méthode sélectionnée : {method} - linéarité de l'intégrale"
            ))
        elif isinstance(expr, Pow) and expr.exp.is_Number and expr.exp != -1:
            method = self.INTEGRATION_METHODS['direct']
            self.steps.append(self._create_step(
                f"Méthode sélectionnée : {method} - règle de puissance"
            ))
        elif self.is_quotient(expr):
            method = self.INTEGRATION_METHODS['partial_fractions']
            self.steps.append(self._create_step(
                f"Méthode sélectionnée : {method} - fonction rationnelle"
            ))
        elif isinstance(expr, Mul) and len(expr.args) == 2:
            method = self.INTEGRATION_METHODS['parts']
            self.steps.append(self._create_step(
                f"Méthode sélectionnée : {method} - produit de fonctions"
            ))
        else:
            method = self.INTEGRATION_METHODS['direct']
            self.steps.append(self._create_step(
                f"Méthode sélectionnée : {method} - intégration directe"
            ))
        
        return method

    def _compute_antiderivative(self, expr, var, method):
        """ÉTAPE 5: Calcule la primitive étape par étape"""
        self.steps.append(self._create_step("Calcul de la primitive :"))
        
        if method == self.INTEGRATION_METHODS['direct']:
            primitive = self._handle_direct_integration(expr, var)
        elif method == self.INTEGRATION_METHODS['parts']:
            primitive = self._handle_integration_by_parts(expr, var)
        elif method == self.INTEGRATION_METHODS['partial_fractions']:
            primitive = self._handle_partial_fractions(expr, var)
        else:
            primitive = self._handle_direct_integration(expr, var)
        
        return primitive

    def _handle_direct_integration(self, expr, var):
        """Gère l'intégration directe"""
        if expr.is_Number:
            # Intégration d'une constante
            self.steps.append(self._create_step(
                "On utilise la formule :", 
                self.INTEGRATION_FORMULAS['constant']
            ))
            primitive = expr * var
            self.steps.append(self._create_step(
                "Résultat :", 
                f"\\int {latex(expr)} dx = {latex(primitive)} + C"
            ))
        
        elif isinstance(expr, Add):
            # Linéarité de l'intégrale
            self.steps.append(self._create_step(
                "On utilise la linéarité :", 
                self.INTEGRATION_FORMULAS['sum']
            ))
            
            primitives = []
            for i, term in enumerate(expr.args, 1):
                term_primitive = integrate(term, var)
                primitives.append(term_primitive)
                self.steps.append(self._create_step(
                    f"Terme {i} :", 
                    f"$\\int {latex(term)} dx = {latex(term_primitive)} + C$"
                ))
            
            primitive = sum(primitives, S.Zero)
            self.steps.append(self._create_step(
                "Résultat final :", 
                f"$\\int {latex(expr)} dx = {latex(primitive)} + C$"
            ))
        
        elif isinstance(expr, Pow) and expr.exp.is_Number and expr.exp != -1:
            # Règle de puissance
            base, expn = expr.args
            self.steps.append(self._create_step(
                "On utilise la règle de puissance :", 
                self.INTEGRATION_FORMULAS['power']
            ))
            
            if expn == 0:
                primitive = var
            else:
                new_exp = expn + 1
                primitive = (base ** new_exp) / new_exp
            
            self.steps.append(self._create_step(
                "Résultat :", 
                f"$\\int {latex(expr)} dx = {latex(primitive)} + C$"
            ))
        
        else:
            # Intégration générale
            primitive = integrate(expr, var)
            self.steps.append(self._create_step(
                "Résultat :", 
                f"$\\int {latex(expr)} dx = {latex(primitive)} + C$"
            ))
        
        return primitive

    def _handle_integration_by_parts(self, expr, var):
        """Gère l'intégration par parties"""
        self.steps.append(self._create_step(
            "On utilise l'intégration par parties :", 
            "$\\int u dv = uv - \\int v du$"
        ))
        
        # Pour l'instant, on utilise l'intégration directe de SymPy
        primitive = integrate(expr, var)
        self.steps.append(self._create_step(
            "Résultat :", 
            f"$\\int {latex(expr)} dx = {latex(primitive)} + C$"
        ))
        
        return primitive

    def _handle_partial_fractions(self, expr, var):
        """Gère la décomposition en fractions partielles"""
        self.steps.append(self._create_step(
            "On utilise la décomposition en fractions partielles"
        ))
        
        # Pour l'instant, on utilise l'intégration directe de SymPy
        primitive = integrate(expr, var)
        self.steps.append(self._create_step(
            "Résultat :", 
            f"$\\int {latex(expr)} dx = {latex(primitive)} + C$"
        ))
        
        return primitive

    def _calculate_final_result(self, primitive, var, lower_bound, upper_bound, integral_type):
        """ÉTAPE 6 & 7: Calcule le résultat final"""
        if integral_type == self.INTEGRAL_TYPES['definite']:
            # ÉTAPE 6: Application des bornes pour intégrale définie
            self.steps.append(self._create_step(
                "Application des bornes d'intégration :"
            ))
            
            try:
                lower_val = float(lower_bound) if lower_bound != '-oo' else -oo
                upper_val = float(upper_bound) if upper_bound != 'oo' else oo
                
                result = integrate(primitive, (var, lower_val, upper_val))
                self.steps.append(self._create_step(
                    f"Évaluation en {upper_bound} :", 
                    f"${latex(primitive.subs(var, upper_val))}$"
                ))
                self.steps.append(self._create_step(
                    f"Évaluation en {lower_bound} :", 
                    f"${latex(primitive.subs(var, lower_val))}$"
                ))
                self.steps.append(self._create_step(
                    "Résultat final :", 
                    f"$\\int_{{{lower_bound}}}^{{{upper_bound}}} ... dx = {latex(result)}$"
                ))
                
            except Exception as e:
                result = f"\\int_{{{lower_bound}}}^{{{upper_bound}}} ... dx = {latex(primitive)}"
                self.steps.append(self._create_step(
                    "Résultat :", 
                    f"Primitive : ${latex(primitive)} + C$"
                ))
        else:
            # Intégrale indéfinie
            result = latex(primitive) + " + C"
            self.steps.append(self._create_step(
                "Résultat final :", 
                f"$\\int ... dx = {result}$"
            ))
        
        return result

    def _create_step(self, text=None, formula=None):
        """Crée une étape avec texte et formule en LaTeX"""
        if formula:
            formula = f"$$ {formula} $$"
        return {'text': text, 'formula': formula}

    def is_quotient(self, expr):
        """Détecte si l'expression est un quotient (fraction)"""
        if hasattr(expr, 'as_numer_denom'):
            numer, denom = expr.as_numer_denom()
            if denom != S.One:
                return True
        
        if isinstance(expr, Mul):
            for arg in expr.args:
                if isinstance(arg, Pow) and arg.exp.is_negative:
                    return True
        
        if isinstance(expr, Pow) and expr.exp.is_negative:
            return True
        
        if isinstance(expr, Mul) and len(expr.args) == 2:
            for arg in expr.args:
                if isinstance(arg, Pow) and arg.exp.is_negative:
                    return True
        
        return False 