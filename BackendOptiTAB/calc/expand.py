from sympy import symbols, expand, simplify, latex, Add, Mul, Pow
from sympy.parsing.latex import parse_latex


class ExpandCalculator:
    """Calculateur de développement avec étapes détaillées et pédagogiques"""
    
    # Constantes pour les types d'expressions
    EXPRESSION_TYPES = {
        'notable_identity': "identité remarquable",
        'binomial_product': "produit de binômes",
        'polynomial_product': "produit de polynômes",
        'simple_product': "produit simple",
        'power': "puissance",
        'complex': "expression complexe"
    }
    
    # Identités remarquables connues
    NOTABLE_IDENTITIES = {
        'square_sum': "(a + b)² = a² + 2ab + b²",
        'square_diff': "(a - b)² = a² - 2ab + b²", 
        'product_sum_diff': "(a + b)(a - b) = a² - b²",
        'cube_sum': "(a + b)³ = a³ + 3a²b + 3ab² + b³",
        'cube_diff': "(a - b)³ = a³ - 3a²b + 3ab² - b³"
    }

    def __init__(self):
        self.steps = []

    def calculate_expansion(self, expr_latex):
        """Calcule le développement avec étapes détaillées"""
        print(f"Traitement de l'expression: {expr_latex}")
        
        # ÉTAPE 1: PARSING DE L'EXPRESSION
        expr = self._parse_expression(expr_latex)
        self.steps = []
        
        # ÉTAPE 2: ANALYSE DE LA STRUCTURE
        self.steps.append(self._create_step(f"On développe l'expression : ${expr_latex}$"))
        expression_type = self._identify_expression_type(expr)
        self.steps.append(self._create_step(f"Type d'expression identifié : {expression_type}"))

        # ÉTAPE 3: APPLICATION DES MÉTHODES DE DÉVELOPPEMENT
        result_steps = self._apply_expansion_methods(expr, expr_latex)
        self.steps.extend(result_steps)

        # ÉTAPE 4: SIMPLIFICATION ET RÉSULTAT FINAL
        final_result = self._calculate_final_result(expr, expr_latex)

        print(f"Résultat final: {final_result}")
        print(f"Nombre d'étapes: {len(self.steps)}")

        return {'result_latex': final_result, 'steps': self.steps}

    def _parse_expression(self, expr_latex):
        """Parse l'expression LaTeX"""
        try:
            expr = parse_latex(expr_latex)
            print(f"Expression parsée: {expr}")
            return expr
        except Exception as parse_error:
            print(f"Erreur parsing: {parse_error}")
            raise ValueError(f'Erreur de parsing LaTeX: {str(parse_error)}')

    def _identify_expression_type(self, expr):
        """Identifie le type d'expression"""
        # On identifie via la structure sympy
        if self._is_notable_identity(expr):
            return self.EXPRESSION_TYPES['notable_identity']
        elif self._is_binomial_product(expr):
            return self.EXPRESSION_TYPES['binomial_product']
        elif isinstance(expr, Pow) and isinstance(expr.base, Add):
            return self.EXPRESSION_TYPES['power']
        elif isinstance(expr, Mul) and len(expr.args) > 2:
            return self.EXPRESSION_TYPES['polynomial_product']
        elif isinstance(expr, Mul) and len(expr.args) == 2:
            return self.EXPRESSION_TYPES['simple_product']
        else:
            return self.EXPRESSION_TYPES['complex']

    def _is_notable_identity(self, expr):
        """Vérifie si c'est une identité remarquable"""
        # (a+b)^2 ou (a-b)^2
        if isinstance(expr, Pow) and expr.exp == 2:
            base = expr.base
            if isinstance(base, Add) and len(base.args) == 2:
                return True
        # (a+b)(a-b)
        elif isinstance(expr, Mul) and len(expr.args) == 2:
            if all(isinstance(arg, Add) and len(arg.args) == 2 for arg in expr.args):
                # Vérifier si l'un est la soustraction de l'autre
                a1, a2 = expr.args[0].args
                b1, b2 = expr.args[1].args
                if a1 == b1 and a2 == -b2:
                    return True
        return False

    def _is_binomial_product(self, expr):
        """Vérifie si c'est un produit de binômes (pas forcément conjugués)"""
        if isinstance(expr, Mul) and len(expr.args) == 2:
            return all(isinstance(arg, Add) and len(arg.args) == 2 for arg in expr.args)
        return False

    def _apply_expansion_methods(self, expr, expr_latex):
        """Applique les méthodes de développement appropriées"""
        if self._is_notable_identity(expr):
            return self._handle_notable_identity(expr, expr_latex)
        elif self._is_binomial_product(expr):
            return self._handle_binomial_product(expr, expr_latex)
        elif isinstance(expr, Pow) and isinstance(expr.base, Add):
            return self._handle_power_expansion(expr, expr_latex)
        else:
            return self._handle_general_expansion(expr, expr_latex)

    def _handle_notable_identity(self, expr, expr_latex):
        """Gère les identités remarquables avec étapes détaillées"""
        steps = []

        if isinstance(expr, Pow) and expr.exp == 2:
            base = expr.base
            if isinstance(base, Add) and len(base.args) == 2:
                a, b = base.args
                # On vérifie si b est négatif
                if b.is_Number and b < 0:
                    b_pos = -b
                    steps.append(self._create_step(
                        "On applique l'identité remarquable : $(a - b)^2 = a^2 - 2ab + b^2$",
                        f"${expr_latex} = {latex(a)}^2 - 2 \\times {latex(a)} \\times {latex(b_pos)} + {latex(b_pos)}^2$"
                    ))
                    a_squared = expand(a**2)
                    ab_term = expand(2 * a * b_pos)
                    b_squared = expand(b_pos**2)
                    steps.append(self._create_step(
                        "On calcule chaque terme de l'identité",
                        f"${latex(a)}^2 = {latex(a_squared)}$, $2 \\times {latex(a)} \\times {latex(b_pos)} = {latex(ab_term)}$, ${latex(b_pos)}^2 = {latex(b_squared)}$"
                    ))
                    final_result = expand(a_squared - ab_term + b_squared)
                    steps.append(self._create_step(
                        "On combine tous les termes",
                        f"${latex(a_squared)} - {latex(ab_term)} + {latex(b_squared)} = {latex(final_result)}$"
                    ))
                else:
                    # Cas (a + b)^2
                    steps.append(self._create_step(
                        "On applique l'identité remarquable : $(a + b)^2 = a^2 + 2ab + b^2$",
                        f"${expr_latex} = {latex(a)}^2 + 2 \\times {latex(a)} \\times {latex(b)} + {latex(b)}^2$"
                    ))
                    a_squared = expand(a**2)
                    ab_term = expand(2 * a * b)
                    b_squared = expand(b**2)
                    steps.append(self._create_step(
                        "On calcule chaque terme de l'identité",
                        f"${latex(a)}^2 = {latex(a_squared)}$, $2 \\times {latex(a)} \\times {latex(b)} = {latex(ab_term)}$, ${latex(b)}^2 = {latex(b_squared)}$"
                    ))
                    final_result = expand(a_squared + ab_term + b_squared)
                    steps.append(self._create_step(
                        "On combine tous les termes",
                        f"${latex(a_squared)} + {latex(ab_term)} + {latex(b_squared)} = {latex(final_result)}$"
                    ))

        elif isinstance(expr, Mul) and len(expr.args) == 2:
            # (a+b)(a-b)
            if all(isinstance(arg, Add) and len(arg.args) == 2 for arg in expr.args):
                a1, a2 = expr.args[0].args
                b1, b2 = expr.args[1].args
                if a1 == b1 and a2 == -b2:
                    steps.append(self._create_step(
                        "On applique l'identité remarquable : $(a + b)(a - b) = a^2 - b^2$",
                        f"${expr_latex} = {latex(a1)}^2 - {latex(a2)}^2$"
                    ))
                    a1_squared = expand(a1**2)
                    a2_squared = expand(a2**2)
                    steps.append(self._create_step(
                        "On calcule chaque terme de l'identité",
                        f"${latex(a1)}^2 = {latex(a1_squared)}$, ${latex(a2)}^2 = {latex(a2_squared)}$"
                    ))
                    final_result = expand(a1_squared - a2_squared)
                    steps.append(self._create_step(
                        "On soustrait les deux termes",
                        f"${latex(a1_squared)} - {latex(a2_squared)} = {latex(final_result)}$"
                    ))

        return steps

    def _handle_binomial_product(self, expr, expr_latex):
        """Développe un produit de binômes simple"""
        steps = []
        steps.append(self._create_step(f"On développe le produit de binômes : ${expr_latex}$"))
        expanded = expand(expr)
        steps.append(self._create_step("On applique la distributivité", f"${expr_latex} = {latex(expanded)}$"))
        return steps

    def _handle_power_expansion(self, expr, expr_latex):
        """Développe une puissance d'une somme"""
        steps = []
        steps.append(self._create_step(f"On développe la puissance : ${expr_latex}$"))
        expanded = expand(expr)
        steps.append(self._create_step("En utilisant la formule du binôme de Newton", f"${expr_latex} = {latex(expanded)}$"))
        return steps

    def _handle_general_expansion(self, expr, expr_latex):
        """Développe une expression plus complexe"""
        steps = []
        steps.append(self._create_step(f"Développement général de l'expression : ${expr_latex}$"))
        expanded = expand(expr)
        steps.append(self._create_step("Résultat développé", f"${latex(expanded)}$"))
        return steps

    def _calculate_final_result(self, expr, expr_latex):
        """Calcule le résultat final simplifié"""
        expanded = expand(expr)
        simplified = simplify(expanded)
        return latex(simplified)

    def _create_step(self, text=None, formula=None):
        """Crée une étape avec texte et/ou formule"""
        step = {}
        if text:
            step['text'] = text
        if formula:
            step['formula'] = formula
        return step
