from sympy import symbols, diff, simplify, latex, Add, Mul, Pow, S, E, expand, factor
from sympy.functions import sin, cos, tan, exp, log, sqrt
from sympy.parsing.latex import parse_latex


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
        'quotient': "$(\\frac{u}{v})' = \\frac{u'v - uv'}{v^2}$",
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
        print(f"Traitement de l'expression: {expr_latex}")
        
        # ÉTAPE 1: PARSING DE LA FONCTION
        expr, var = self._parse_expression(expr_latex)
        self.steps = []
        
        # ÉTAPE 2: ANALYSE DE LA STRUCTURE
        self.steps.append(self._create_step(f"On calcule $\\frac{{d}}{{dx}}({expr_latex})$"))
        structure_type = self._identify_structure(expr)
        self.steps.append(self._create_step(f"Type de structure identifié : {structure_type}"))

        # ÉTAPE 3: SIMPLIFICATION SI POSSIBLE
        expr, expr_latex = self._simplify_expression(expr, expr_latex)

        # ÉTAPE 4: APPLICATION DES RÈGLES DE DÉRIVATION
        self.steps.extend(self._apply_differentiation_rules(expr, var))

        # ÉTAPE 5 & 6: CALCUL ET SIMPLIFICATION FINALE
        result = self._calculate_final_result(expr, var, expr_latex)

        print(f"Résultat final: {result}")
        print(f"Nombre d'étapes: {len(self.steps)}")

        return {'result_latex': result, 'steps': self.steps}

    def _parse_expression(self, expr_latex):
        """Parse l'expression LaTeX et retourne l'expression et la variable"""
        try:
            expr = parse_latex(expr_latex)
            print(f"Expression parsée: {expr}")
        except Exception as parse_error:
            print(f"Erreur parsing: {parse_error}")
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
        self.steps.append(self._create_step(
            "On calcule la dérivée :", 
            f"\\frac{{d}}{{dx}}({expr_latex}) = {latex(deriv)}"
        ))

        # ÉTAPE 6: SIMPLIFICATION DU RÉSULTAT FINAL
        deriv_simplified = simplify(deriv)
        result = latex(deriv_simplified)
        
        if deriv != deriv_simplified:
            self.steps.append(self._create_step(
                "On simplifie le résultat final :", 
                f"{latex(deriv)} = {result}"
            ))
        else:
            self.steps.append(self._create_step("Résultat final :", result))
        
        return result

    def _create_step(self, text=None, formula=None):
        """Crée une étape avec texte et formule en LaTeX"""
        if formula:
            formula = f"$$ {formula} $$"
        return {'text': text, 'formula': formula}

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
        """Ajoute des parenthèses autour du LaTeX si nécessaire"""
        if hasattr(expr, 'as_numer_denom') and expr.as_numer_denom()[1] != S.One:
            return f'\\left({latex(expr)}\\right)'
        elif isinstance(expr, Add) or (expr.is_Mul and len(expr.args) > 1) or expr.is_Pow:
            return f'\\left({latex(expr)}\\right)'
        return latex(expr)

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
        u_latex = self._force_parens(u)
        v_latex = self._force_parens(v)
        
        steps.append(self._create_step(
            "On utilise la règle du produit :", 
            self.DERIVATION_FORMULAS['product']
        ))
        steps.append(self._create_step(f"On pose $u = {u_latex}$ et $v = {v_latex}$"))
        
        d_u = diff(u, var)
        d_v = diff(v, var)
        
        steps.append(self._create_step(f"On calcule $u' = {latex(d_u)}$"))
        steps.append(self._create_step(f"On calcule $v' = {latex(d_v)}$"))
        
        result_latex = f"{latex(d_u)} \\cdot {v_latex} + {u_latex} \\cdot {latex(d_v)}"
        steps.append(self._create_step(
            "On remplace dans la formule :", 
            f"({u_latex} \\cdot {v_latex})' = {result_latex}"
        ))
        
        return steps

    def _handle_quotient_rule(self, expr, var):
        """Applique la règle du quotient"""
        steps = []
        numer, denom = expr.as_numer_denom()
        u_latex = self._force_parens(numer)
        v_latex = self._force_parens(denom)
        
        steps.append(self._create_step(
            "On utilise la règle du quotient :", 
            self.DERIVATION_FORMULAS['quotient']
        ))
        steps.append(self._create_step(f"On pose $u = {u_latex}$ et $v = {v_latex}$"))
        
        d_u = diff(numer, var)
        d_v = diff(denom, var)
        
        steps.append(self._create_step(f"On calcule $u' = {latex(d_u)}$"))
        steps.append(self._create_step(f"On calcule $v' = {latex(d_v)}$"))
        
        result_latex = f"\\frac{{{latex(d_u)} \\cdot {v_latex} - {u_latex} \\cdot {latex(d_v)}}}{{({v_latex})^2}}"
        steps.append(self._create_step(
            "On remplace dans la formule :", 
            f"(\\frac{{{u_latex}}}{{{v_latex}}})' = {result_latex}"
        ))
        
        return steps

    def _handle_power_rule(self, expr, var):
        """Applique la règle de la puissance"""
        steps = []
        base, expn = expr.args
        base_latex = self._force_parens(base)
        
        if expn.is_Number:
            steps.append(self._create_step(
                "On utilise la règle de la puissance :", 
                self.DERIVATION_FORMULAS['power']
            ))
            steps.append(self._create_step(f"On pose $u = {base_latex}$ et $n = {latex(expn)}$"))
            
            d_base = diff(base, var)
            steps.append(self._create_step(f"On calcule $u' = {latex(d_base)}$"))
            
            result_latex = f"{latex(expn)} \\cdot {base_latex}^{{{latex(expn-1)}}} \\cdot {latex(d_base)}"
            steps.append(self._create_step(
                "On remplace dans la formule :", 
                f"({base_latex}^{{{latex(expn)}}})' = {result_latex}"
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