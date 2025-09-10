from sympy import symbols, diff, simplify, latex, Add, Mul, Pow, S, E, expand, factor
from sympy.functions import sin, cos, tan, exp, log, sqrt
from sympy.parsing.latex import parse_latex
import logging


logger = logging.getLogger(__name__)


class DerivativeCalculator:
    """Calculateur de dérivées avec étapes détaillées"""
    
    # Constantes pour les types de structure
    STRUCTURE_TYPES = {
        'add': "somme/soustraction",
        'quotient': "quotient", 
        'product': "produit",
        'power': "puissance",
        'function': "fonction élémentaire",
        'variable': "variable",
        'constant': "constante",
        'complex': "expression complexe"
    }
    
    # Constantes pour les formules de dérivation
    DERIVATION_FORMULAS = {
        'sum': "$(u + v)' = u' + v'$",
        'product': "$(uv)' = u'v + uv'$",
        'quotient': "$\\left(\\frac{u}{v}\\right)' = \\frac{u'v - uv'}{v^2}$",
        'power': "$(u^n)' = n \\cdot u^{n-1} \\cdot u'$",
        'sin': "$(\\sin(u))' = \\cos(u) \\cdot u'$",
        'cos': "$(\\cos(u))' = -\\sin(u) \\cdot u'$",
        'exp': "$(e^u)' = e^u \\cdot u'$",
        'log': "$(\\ln(u))' = \\frac{u'}{u}$"
    }

    def __init__(self):
        self.steps = []

    def calculate_derivative(self, expr_latex):
        """Calcule la dérivée avec étapes détaillées"""
        logger.debug(f"Traitement de l'expression: {expr_latex}")
        
        # ÉTAPE 1: PARSING DE LA FONCTION
        expr, var = self._parse_expression(expr_latex)
        self.steps = []
        
        # ÉTAPE 2: ANALYSE DE LA STRUCTURE
        # Formatage avec une seule paire de grandes parenthèses pour l'étape 1
        formatted_expr = latex(expr)
        self.steps.append(self._create_step(f"On calcule $\\frac{{d}}{{dx}}\\left({formatted_expr}\\right)$"))
        structure_type = self._identify_structure(expr)
        self.steps.append(self._create_step(f"Type de structure identifié : {structure_type}"))

        # ÉTAPE 3: SIMPLIFICATION SI POSSIBLE
        expr, expr_latex = self._simplify_expression(expr, expr_latex)

        # ÉTAPE 4: APPLICATION DES RÈGLES DE DÉRIVATION
        self.steps.extend(self._apply_differentiation_rules(expr, var))

        # ÉTAPE 5 & 6: CALCUL ET SIMPLIFICATION FINALE
        result = self._calculate_final_result(expr, var, expr_latex)

        logger.debug(f"Résultat final: {result}; étapes: {len(self.steps)}")

        return {'result_latex': result, 'steps': self.steps}

    def _parse_expression(self, expr_latex):
        """Parse l'expression LaTeX et retourne l'expression et la variable"""
        try:
            expr = parse_latex(expr_latex)
            logger.debug(f"Expression parsée: {expr}")
        except Exception as parse_error:
            logger.error(f"Erreur parsing: {parse_error}")
            raise ValueError(f'Erreur de parsing LaTeX: {str(parse_error)}')
        
        expr = expr.subs(symbols('e'), E)
        var = list(expr.free_symbols)[0] if expr.free_symbols else symbols('x')
        return expr, var

    def _identify_structure(self, expr):
        """Identifie le type de structure de l'expression"""
        if isinstance(expr, Add):
            return self.STRUCTURE_TYPES['add']
        elif self.is_quotient(expr):
            return self.STRUCTURE_TYPES['quotient']
        elif isinstance(expr, Mul) and len(expr.args) == 2:
            return self.STRUCTURE_TYPES['product']
        elif isinstance(expr, Pow):
            return self.STRUCTURE_TYPES['power']
        elif hasattr(expr, 'func') and len(expr.args) == 1:
            return self.STRUCTURE_TYPES['function']
        elif expr == symbols('x'):
            return self.STRUCTURE_TYPES['variable']
        elif expr.is_Number:
            return self.STRUCTURE_TYPES['constant']
        else:
            return self.STRUCTURE_TYPES['complex']

    def _simplify_expression(self, expr, expr_latex):
        """Simplifie l'expression si possible"""
        expr_original = expr
        expr_simplified = simplify(expr)
        
        if expr != expr_simplified:
            self.steps.append(self._create_step(
                "On simplifie l'expression avant dérivation :", 
                f"{latex(expr)} = {latex(expr_simplified)}"
            ))
            expr = expr_simplified
            expr_latex = latex(expr)
        
        return expr, expr_latex

    def _calculate_final_result(self, expr, var, expr_latex):
        """Calcule le résultat final et simplifie"""
        # ÉTAPE 5: CALCUL DE LA DÉRIVÉE
        deriv = diff(expr, var)
        
        # Utiliser des grandes parenthèses pour l'étape de calcul
        deriv_latex = self._latex_with_large_parens(deriv)
        
        self.steps.append(self._create_step(
            "On calcule la dérivée :", 
            f"\\frac{{d}}{{dx}}\\left({latex(expr)}\\right) = {deriv_latex}"
        ))

        # ÉTAPE 6: SIMPLIFICATION ET FACTORISATION DU RÉSULTAT FINAL
        deriv_simplified = simplify(deriv)
        
        # Essayons aussi la factorisation
        deriv_factored = factor(deriv)
        
        # On choisit la forme la plus compacte et lisible
        if deriv_factored != deriv and len(latex(deriv_factored)) <= len(latex(deriv)):
            result = self._latex_with_large_parens(deriv_factored)
            self.steps.append(self._create_step(
                "On factorise pour obtenir la forme finale :", 
                f"{deriv_latex} = {result}"
            ))
        elif deriv != deriv_simplified:
            result = self._latex_with_large_parens(deriv_simplified)
            self.steps.append(self._create_step(
                "On simplifie le résultat :", 
                f"{deriv_latex} = {result}"
            ))
        else:
            result = deriv_latex
            self.steps.append(self._create_step("Résultat final :", result))
        
        return result

    def _create_step(self, text=None, formula=None):
        """Crée une étape avec texte et formule en LaTeX"""
        if formula:
            formula = f"$$ {formula} $$"
        return {'text': text, 'formula': formula}

    def _calculate_derivative_detailed(self, expr, var, var_name=""):
        """Calcule la dérivée d'une expression avec toutes les étapes détaillées"""
        steps = []
        
        if isinstance(expr, Pow):
            base, expn = expr.args
            base_latex = self._force_parens(base)
            
            if expn.is_Number:
                steps.append(self._create_step(
                    f"Pour ${var_name} = {latex(expr)}$, on utilise la règle de la puissance :",
                    f"(u^n)' = n \\cdot u^{{n-1}} \\cdot u'"
                ))
                steps.append(self._create_step(f"Ici, $u = {base_latex}$ et $n = {latex(expn)}$"))
                
                if base == var:
                    steps.append(self._create_step(f"$u' = \\frac{{d}}{{dx}}({base_latex}) = 1$"))
                elif isinstance(base, Add):
                    # Cas comme (x + 3) ou (9x + 7)
                    d_base = diff(base, var)
                    steps.append(self._create_step(f"$u' = \\frac{{d}}{{dx}}({base_latex}) = {latex(d_base)}$"))
                else:
                    d_base = diff(base, var)
                    steps.append(self._create_step(f"$u' = \\frac{{d}}{{dx}}({base_latex}) = {latex(d_base)}$"))
                
                d_base = diff(base, var)
                result_latex = f"{latex(expn)} \\cdot {base_latex}^{{{latex(expn-1)}}} \\cdot {latex(d_base)}"
                steps.append(self._create_step(
                    f"Donc :",
                    f"{var_name}' = {result_latex}"
                ))
                
                # Simplification si possible
                final_result = diff(expr, var)
                if latex(final_result) != result_latex:
                    steps.append(self._create_step(
                        f"En simplifiant :",
                        f"{var_name}' = {latex(final_result)}"
                    ))
        
        elif isinstance(expr, Add):
            terms = expr.args
            steps.append(self._create_step(
                f"Pour ${var_name} = {latex(expr)}$, on dérive terme par terme :"
            ))
            
            derivs = []
            for i, term in enumerate(terms, 1):
                d_term = diff(term, var)
                steps.append(self._create_step(f"Terme {i}: $\\frac{{d}}{{dx}}({latex(term)}) = {latex(d_term)}$"))
                derivs.append(latex(d_term))
            
            result_latex = " + ".join(derivs)
            steps.append(self._create_step(
                f"Donc :",
                f"{var_name}' = {result_latex}"
            ))
            
            # Simplification
            final_result = diff(expr, var)
            steps.append(self._create_step(
                f"En simplifiant :",
                f"{var_name}' = {latex(final_result)}"
            ))
        
        else:
            # Cas général
            d_expr = diff(expr, var)
            steps.append(self._create_step(f"{var_name}' = \\frac{{d}}{{dx}}({latex(expr)}) = {latex(d_expr)}"))
        
        return steps

    def is_quotient(self, expr):
        """Détecte si l'expression est un quotient (fraction)"""
        # Méthode 1: Vérifier si c'est déjà un quotient explicite
        if hasattr(expr, 'as_numer_denom'):
            numer, denom = expr.as_numer_denom()
            if denom != S.One:
                return True
        
        # Méthode 2: Vérifier si c'est un produit avec une puissance négative
        if isinstance(expr, Mul):
            for arg in expr.args:
                if isinstance(arg, Pow) and arg.exp.is_negative:
                    return True
        
        # Méthode 3: Vérifier si c'est une puissance négative directe
        if isinstance(expr, Pow) and expr.exp.is_negative:
            return True
        
        # Méthode 4: Vérifier si c'est un produit qui peut être réécrit comme quotient
        if isinstance(expr, Mul) and len(expr.args) == 2:
            for arg in expr.args:
                if isinstance(arg, Pow) and arg.exp.is_negative:
                    return True
        
        return False

    def _force_parens(self, expr):
        """Ajoute des parenthèses adaptatives autour du LaTeX si nécessaire"""
        if hasattr(expr, 'as_numer_denom') and expr.as_numer_denom()[1] != S.One:
            return f'\\left({latex(expr)}\\right)'
        elif isinstance(expr, Add) or (expr.is_Mul and len(expr.args) > 1) or expr.is_Pow:
            return f'\\left({latex(expr)}\\right)'
        return latex(expr)

    def _format_fraction(self, numerator, denominator):
        """Formate une fraction avec des parenthèses adaptatives"""
        num_latex = latex(numerator) if not isinstance(numerator, (Add, Mul)) else f'\\left({latex(numerator)}\\right)'
        den_latex = latex(denominator) if not isinstance(denominator, (Add, Mul)) else f'\\left({latex(denominator)}\\right)'
        return f'\\frac{{{num_latex}}}{{{den_latex}}}'

    def _format_large_parens(self, expr):
        """Formate une expression avec des grandes parenthèses adaptatives"""
        return f'\\left({latex(expr)}\\right)'

    def _latex_with_large_parens(self, expr):
        """Génère du LaTeX avec grandes parenthèses pour toutes les parenthèses"""
        import re
        latex_str = latex(expr)
        
        # Remplacer toutes les parenthèses par des grandes parenthèses
        # Technique itérative pour gérer les expressions imbriquées
        max_iterations = 10
        for _ in range(max_iterations):
            prev_latex = latex_str
            
            # Pattern 1: Parenthèses avec exposant (x + 3)^2 -> \left(x + 3\right)^2
            latex_str = re.sub(r'(?<!\\left)\(([^()]*)\)\^(\{?[^{}]*\}?)', r'\\left(\1\\right)^{\2}', latex_str)
            
            # Pattern 2: Parenthèses simples sans exposant (x + 2) -> \left(x + 2\right)
            latex_str = re.sub(r'(?<!\\left)(?<!\\right)\(([^()]*)\)(?!\^)', r'\\left(\1\\right)', latex_str)
            
            # Si aucun changement, on arrête
            if prev_latex == latex_str:
                break
        
        return latex_str

    def _handle_sum_rule(self, expr, var):
        """Applique la règle de la somme"""
        steps = []
        steps.append(self._create_step(
            "On utilise la règle de la somme :", 
            self.DERIVATION_FORMULAS['sum']
        ))
        
        terms_formula = ' + '.join([f'({latex(arg)})' + "'" for arg in expr.args])
        steps.append(self._create_step(
            f"On dérive chaque terme séparément : $({latex(expr)})' = {terms_formula}$"
        ))
        
        for i, arg in enumerate(expr.args, 1):
            arg_latex = latex(arg)
            d_arg = diff(arg, var)
            steps.append(self._create_step(
                f"Terme {i} : la dérivée de ${arg_latex}$ est ${latex(d_arg)}$"
            ))
        
        return steps

    def _handle_product_rule(self, expr, var):
        """Applique la règle du produit"""
        steps = []
        u, v = expr.args
        u_latex = self._format_large_parens(u)
        v_latex = self._format_large_parens(v)
        
        steps.append(self._create_step(
            "On utilise la règle du produit :", 
            self.DERIVATION_FORMULAS['product']
        ))
        steps.append(self._create_step(f"On pose $u = {u_latex}$ et $v = {v_latex}$"))
        
        # Calcul détaillé de u'
        steps.append(self._create_step("Calcul de $u'$ :"))
        if isinstance(u, Pow):
            steps.extend(self._calculate_derivative_detailed(u, var, "u"))
        else:
            d_u = diff(u, var)
            steps.append(self._create_step(f"$u' = \\frac{{d}}{{dx}}{u_latex} = {latex(d_u)}$"))
        
        # Calcul détaillé de v'
        steps.append(self._create_step("Calcul de $v'$ :"))
        if isinstance(v, Pow):
            steps.extend(self._calculate_derivative_detailed(v, var, "v"))
        else:
            d_v = diff(v, var)
            steps.append(self._create_step(f"$v' = \\frac{{d}}{{dx}}{v_latex} = {latex(d_v)}$"))
        
        # Récupération des résultats
        d_u = diff(u, var)
        d_v = diff(v, var)
        
        result_latex = f"{latex(d_u)} \\cdot {v_latex} + {u_latex} \\cdot {latex(d_v)}"
        steps.append(self._create_step(
            "On remplace dans la formule :", 
            f"\\left({u_latex} \\cdot {v_latex}\\right)' = {result_latex}"
        ))
        
        return steps

    def _handle_quotient_rule(self, expr, var):
        """Applique la règle du quotient"""
        steps = []
        numer, denom = expr.as_numer_denom()
        u_latex = self._format_large_parens(numer)
        v_latex = self._format_large_parens(denom)
        
        steps.append(self._create_step(
            "On utilise la règle du quotient :", 
            self.DERIVATION_FORMULAS['quotient']
        ))
        steps.append(self._create_step(f"On pose $u = {u_latex}$ et $v = {v_latex}$"))
        
        d_u = diff(numer, var)
        d_v = diff(denom, var)
        
        steps.append(self._create_step(f"On calcule $u' = {latex(d_u)}$"))
        steps.append(self._create_step(f"On calcule $v' = {latex(d_v)}$"))
        
        # Formule mathématique complète avec grandes parenthèses
        u_prime_latex = self._latex_with_large_parens(d_u)
        v_prime_latex = self._latex_with_large_parens(d_v)
        u_large_latex = self._latex_with_large_parens(numer)
        v_large_latex = self._latex_with_large_parens(denom)
        
        # Calcul mathématique exact de la formule du quotient
        quotient_formula = (d_u * denom - numer * d_v) / (denom**2)
        result_latex = self._latex_with_large_parens(quotient_formula)
        
        steps.append(self._create_step(
            "On remplace dans la formule :", 
            f"\\left(\\frac{{{u_latex}}}{{{v_latex}}}\\right)' = {result_latex}"
        ))
        
        return steps

    def _handle_power_rule(self, expr, var):
        """Applique la règle de la puissance"""
        steps = []
        base, expn = expr.args
        base_latex = self._format_large_parens(base)
        
        if expn.is_Number:
            steps.append(self._create_step(
                "On utilise la règle de la puissance :", 
                self.DERIVATION_FORMULAS['power']
            ))
            steps.append(self._create_step(f"On pose $u = {base_latex}$ et $n = {latex(expn)}$"))
            
            # Calcul détaillé de u'
            if base == var:
                steps.append(self._create_step(f"$u' = \\frac{{d}}{{dx}}{base_latex} = 1$"))
            elif isinstance(base, Add):
                # Décomposition pour les expressions comme (x + 3)
                terms = base.args
                steps.append(self._create_step(f"Pour calculer $u'$, on dérive ${base_latex}$ terme par terme :"))
                
                derivs = []
                for term in terms:
                    d_term = diff(term, var)
                    if term == var:
                        steps.append(self._create_step(f"$\\frac{{d}}{{dx}}\\left({latex(term)}\\right) = 1$"))
                    elif term.is_Number:
                        steps.append(self._create_step(f"$\\frac{{d}}{{dx}}\\left({latex(term)}\\right) = 0$"))
                    else:
                        steps.append(self._create_step(f"$\\frac{{d}}{{dx}}\\left({latex(term)}\\right) = {latex(d_term)}$"))
                    derivs.append(latex(d_term))
                
                d_base = diff(base, var)
                steps.append(self._create_step(f"Donc $u' = {' + '.join(derivs)} = {latex(d_base)}$"))
            else:
                d_base = diff(base, var)
                steps.append(self._create_step(f"$u' = \\frac{{d}}{{dx}}{base_latex} = {latex(d_base)}$"))
            
            d_base = diff(base, var)
            
            # Application de la formule avec grandes parenthèses
            if expn == 2:
                result_latex = f"{latex(expn)} \\cdot {base_latex} \\cdot {latex(d_base)}"
                steps.append(self._create_step(
                    "On remplace dans la formule :", 
                    f"\\left({base_latex}^{{{latex(expn)}}}\\right)' = {latex(expn)} \\cdot {base_latex}^{{{latex(expn-1)}}} \\cdot {latex(d_base)} = {result_latex}"
                ))
            else:
                result_latex = f"{latex(expn)} \\cdot {base_latex}^{{{latex(expn-1)}}} \\cdot {latex(d_base)}"
                steps.append(self._create_step(
                    "On remplace dans la formule :", 
                    f"\\left({base_latex}^{{{latex(expn)}}}\\right)' = {result_latex}"
                ))
        
        return steps

    def _handle_elementary_function(self, expr, var):
        """Applique les règles pour les fonctions élémentaires"""
        steps = []
        arg = expr.args[0]
        func_name = expr.func.__name__
        
        if func_name == 'sin':
            steps.extend(self._handle_sin_function(arg, var))
        elif func_name == 'cos':
            steps.extend(self._handle_cos_function(arg, var))
        elif func_name == 'exp':
            steps.extend(self._handle_exp_function(arg, var))
        elif func_name == 'log':
            steps.extend(self._handle_log_function(arg, var))
        else:
            # Cas générique pour les autres fonctions
            d_expr = diff(expr, var)
            steps.append(self._create_step(
                f"La dérivée de ${latex(expr)}$ est ${latex(d_expr)}$"
            ))
        
        return steps

    def _handle_sin_function(self, arg, var):
        """Gère la dérivée du sinus"""
        steps = []
        steps.append(self._create_step(
            "On utilise la dérivée du sinus :", 
            self.DERIVATION_FORMULAS['sin']
        ))
        steps.append(self._create_step(f"On pose $u = {latex(arg)}$"))
        
        d_arg = diff(arg, var)
        steps.append(self._create_step(f"On calcule $u' = {latex(d_arg)}$"))
        
        result_latex = f"\\cos({latex(arg)}) \\cdot {latex(d_arg)}"
        steps.append(self._create_step(
            "On remplace dans la formule :", 
            f"(\\sin({latex(arg)}))' = {result_latex}"
        ))
        
        return steps

    def _handle_cos_function(self, arg, var):
        """Gère la dérivée du cosinus"""
        steps = []
        steps.append(self._create_step(
            "On utilise la dérivée du cosinus :", 
            self.DERIVATION_FORMULAS['cos']
        ))
        steps.append(self._create_step(f"On pose $u = {latex(arg)}$"))
        
        d_arg = diff(arg, var)
        steps.append(self._create_step(f"On calcule $u' = {latex(d_arg)}$"))
        
        result_latex = f"-\\sin({latex(arg)}) \\cdot {latex(d_arg)}"
        steps.append(self._create_step(
            "On remplace dans la formule :", 
            f"(\\cos({latex(arg)}))' = {result_latex}"
        ))
        
        return steps

    def _handle_exp_function(self, arg, var):
        """Gère la dérivée de l'exponentielle"""
        steps = []
        steps.append(self._create_step(
            "On utilise la dérivée de l'exponentielle :", 
            self.DERIVATION_FORMULAS['exp']
        ))
        steps.append(self._create_step(f"On pose $u = {latex(arg)}$"))
        
        d_arg = diff(arg, var)
        steps.append(self._create_step(f"On calcule $u' = {latex(d_arg)}$"))
        
        result_latex = f"e^{{{latex(arg)}}} \\cdot {latex(d_arg)}"
        steps.append(self._create_step(
            "On remplace dans la formule :", 
            f"(e^{{{latex(arg)}}})' = {result_latex}"
        ))
        
        return steps

    def _handle_log_function(self, arg, var):
        """Gère la dérivée du logarithme"""
        steps = []
        steps.append(self._create_step(
            "On utilise la dérivée du logarithme :", 
            self.DERIVATION_FORMULAS['log']
        ))
        steps.append(self._create_step(f"On pose $u = {latex(arg)}$"))
        
        d_arg = diff(arg, var)
        steps.append(self._create_step(f"On calcule $u' = {latex(d_arg)}$"))
        
        result_latex = f"\\frac{{{latex(d_arg)}}}{{{latex(arg)}}}"
        steps.append(self._create_step(
            "On remplace dans la formule :", 
            f"(\\ln({latex(arg)}))' = {result_latex}"
        ))
        
        return steps

    def _apply_differentiation_rules(self, expr, var):
        """Applique les règles de dérivation selon la structure de l'expression"""
        # Règle de la somme/soustraction
        if isinstance(expr, Add):
            return self._handle_sum_rule(expr, var)

        # Règle du produit (seulement si ce n'est pas un quotient)
        elif isinstance(expr, Mul) and len(expr.args) == 2 and not self.is_quotient(expr):
            return self._handle_product_rule(expr, var)

        # Règle du quotient
        elif self.is_quotient(expr):
            return self._handle_quotient_rule(expr, var)

        # Règle de la puissance
        elif isinstance(expr, Pow):
            return self._handle_power_rule(expr, var)

        # Fonctions élémentaires
        elif hasattr(expr, 'func') and len(expr.args) == 1:
            return self._handle_elementary_function(expr, var)

        # Dérivée de la variable elle-même
        elif expr == var:
            return [self._create_step("La dérivée de $x$ par rapport à $x$ est $1$")]

        # Dérivée d'une constante
        elif expr.is_Number:
            return [self._create_step(f"La dérivée d'une constante ${latex(expr)}$ est $0$")]

        # Cas générique
        else:
            d_expr = diff(expr, var)
            return [self._create_step(f"La dérivée de ${latex(expr)}$ est ${latex(d_expr)}$")] 