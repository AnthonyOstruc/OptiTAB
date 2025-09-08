from sympy import symbols, factor, gcd, expand, simplify, latex, Add, Mul, Pow, S, sqrt
from sympy.parsing.latex import parse_latex
from sympy.polys.polytools import factor_list
from sympy.core.numbers import Integer


class FactorCalculator:
    """Calculateur de factorisation avec étapes détaillées et pédagogiques"""
    
    # Constantes pour les types d'expressions
    EXPRESSION_TYPES = {
        'notable_identity': "identité remarquable",
        'common_factor': "facteur commun",
        'quadratic': "trinôme du second degré",
        'difference_of_squares': "différence de deux carrés",
        'perfect_square': "carré parfait",
        'sum_product': "somme-produit",
        'polynomial': "polynôme",
        'simple': "expression simple",
        'complex': "expression complexe"
    }
    
    # Identités remarquables pour la factorisation
    NOTABLE_PATTERNS = {
        'difference_squares': "a² - b² = (a + b)(a - b)",
        'perfect_square_pos': "a² + 2ab + b² = (a + b)²",
        'perfect_square_neg': "a² - 2ab + b² = (a - b)²",
        'sum_cubes': "a³ + b³ = (a + b)(a² - ab + b²)",
        'difference_cubes': "a³ - b³ = (a - b)(a² + ab + b²)"
    }

    def __init__(self):
        self.steps = []

    def calculate_factorization(self, expr_latex):
        """Calcule la factorisation avec étapes détaillées"""
        print(f"Traitement de l'expression: {expr_latex}")
        
        # ÉTAPE 1: PARSING DE L'EXPRESSION
        expr = self._parse_expression(expr_latex)
        self.steps = []
        
        # ÉTAPE 2: ANALYSE DE LA STRUCTURE
        self.steps.append(self._create_step(f"On factorise l'expression : ${expr_latex}$"))
        expression_type = self._identify_expression_type(expr)
        self.steps.append(self._create_step(f"Type d'expression identifié : {expression_type}"))

        # ÉTAPE 3: APPLICATION DES MÉTHODES DE FACTORISATION
        result_steps = self._apply_factorization_methods(expr, expr_latex)
        self.steps.extend(result_steps)

        # ÉTAPE 4: VÉRIFICATION ET RÉSULTAT FINAL
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
        """Identifie le type d'expression à factoriser"""
        # Différence de deux carrés
        if self._is_difference_of_squares(expr):
            return self.EXPRESSION_TYPES['difference_of_squares']
        # Carré parfait
        elif self._is_perfect_square(expr):
            return self.EXPRESSION_TYPES['perfect_square']
        # Trinôme du second degré
        elif self._is_quadratic(expr):
            return self.EXPRESSION_TYPES['quadratic']
        # Facteur commun
        elif self._has_common_factor(expr):
            return self.EXPRESSION_TYPES['common_factor']
        # Identité remarquable
        elif self._is_notable_identity(expr):
            return self.EXPRESSION_TYPES['notable_identity']
        # Polynôme général
        elif isinstance(expr, Add) and expr.is_polynomial():
            return self.EXPRESSION_TYPES['polynomial']
        # Expression simple
        elif isinstance(expr, (Mul, Pow)):
            return self.EXPRESSION_TYPES['simple']
        else:
            return self.EXPRESSION_TYPES['complex']

    def _is_difference_of_squares(self, expr):
        """Vérifie si c'est une différence de deux carrés (a² - b²)"""
        if isinstance(expr, Add) and len(expr.args) == 2:
            terms = expr.args
            if len(terms) == 2:
                a, b = terms
                # Vérifier si c'est de la forme a² - b² ou -b² + a²
                if (isinstance(a, Pow) and a.exp == 2 and 
                    isinstance(b, Mul) and len(b.args) == 2 and 
                    b.args[0] == -1 and isinstance(b.args[1], Pow) and b.args[1].exp == 2):
                    return True
                elif (isinstance(b, Pow) and b.exp == 2 and 
                      isinstance(a, Mul) and len(a.args) == 2 and 
                      a.args[0] == -1 and isinstance(a.args[1], Pow) and a.args[1].exp == 2):
                    return True
        return False

    def _is_perfect_square(self, expr):
        """Vérifie si c'est un carré parfait (a² ± 2ab + b²)"""
        if isinstance(expr, Add) and len(expr.args) == 3:
            # Essayer de trouver la structure a² + 2ab + b² ou a² - 2ab + b²
            terms = list(expr.args)
            square_terms = []
            linear_term = None
            
            for term in terms:
                if isinstance(term, Pow) and term.exp == 2:
                    square_terms.append(term)
                elif isinstance(term, Mul) and len(term.args) >= 2:
                    # Peut être 2ab ou -2ab
                    linear_term = term
                else:
                    linear_term = term
            
            if len(square_terms) == 2 and linear_term is not None:
                return True
        return False

    def _is_quadratic(self, expr):
        """Vérifie si c'est un trinôme du second degré"""
        if isinstance(expr, Add):
            # Obtenir les variables de l'expression
            variables = list(expr.free_symbols)
            if len(variables) == 1:
                var = variables[0]
                # Vérifier si c'est un polynôme de degré 2
                try:
                    poly = expr.as_poly(var)
                    if poly and poly.degree() == 2:
                        return True
                except:
                    pass
        return False

    def _has_common_factor(self, expr):
        """Vérifie s'il y a un facteur commun"""
        if isinstance(expr, Add):
            terms = expr.args
            if len(terms) >= 2:
                # Calculer le GCD de tous les termes
                try:
                    terms_gcd = gcd(terms)
                    if terms_gcd != 1 and terms_gcd != S.One:
                        return True
                except:
                    pass
        return False

    def _is_notable_identity(self, expr):
        """Vérifie si c'est une identité remarquable spéciale"""
        # Somme ou différence de cubes, etc.
        if isinstance(expr, Add) and len(expr.args) == 2:
            a, b = expr.args
            # a³ + b³ ou a³ - b³
            if (isinstance(a, Pow) and a.exp == 3 and 
                isinstance(b, Pow) and b.exp == 3):
                return True
        return False

    def _apply_factorization_methods(self, expr, expr_latex):
        """Applique les méthodes de factorisation appropriées"""
        if self._is_difference_of_squares(expr):
            return self._handle_difference_of_squares(expr, expr_latex)
        elif self._is_perfect_square(expr):
            return self._handle_perfect_square(expr, expr_latex)
        elif self._is_quadratic(expr):
            return self._handle_quadratic(expr, expr_latex)
        elif self._has_common_factor(expr):
            return self._handle_common_factor(expr, expr_latex)
        elif self._is_notable_identity(expr):
            return self._handle_notable_identity(expr, expr_latex)
        else:
            return self._handle_general_factorization(expr, expr_latex)

    def _handle_difference_of_squares(self, expr, expr_latex):
        """Gère la factorisation d'une différence de deux carrés"""
        steps = []
        steps.append(self._create_step(
            "On reconnaît une différence de deux carrés : $a^2 - b^2 = (a + b)(a - b)$"
        ))
        
        # Identifier a et b
        terms = expr.args
        if len(terms) == 2:
            positive_term = None
            negative_term = None
            
            for term in terms:
                if isinstance(term, Pow) and term.exp == 2:
                    positive_term = term
                elif isinstance(term, Mul) and term.args[0] == -1:
                    negative_term = term.args[1]
            
            if positive_term and negative_term:
                a = positive_term.base
                b = negative_term.base if isinstance(negative_term, Pow) else sqrt(negative_term)
                
                steps.append(self._create_step(
                    f"On identifie : $a = {latex(a)}$ et $b = {latex(b)}$"
                ))
                
                steps.append(self._create_step(
                    "On applique la formule",
                    f"${expr_latex} = ({latex(a)} + {latex(b)})({latex(a)} - {latex(b)})$"
                ))
        
        return steps

    def _handle_perfect_square(self, expr, expr_latex):
        """Gère la factorisation d'un carré parfait"""
        steps = []
        steps.append(self._create_step(
            "On reconnaît un carré parfait : $a^2 \\pm 2ab + b^2 = (a \\pm b)^2$"
        ))
        
        # Utiliser la factorisation sympy pour obtenir le résultat
        factored = factor(expr)
        steps.append(self._create_step(
            "On applique la formule du carré parfait",
            f"${expr_latex} = {latex(factored)}$"
        ))
        
        return steps

    def _handle_quadratic(self, expr, expr_latex):
        """Gère la factorisation d'un trinôme du second degré"""
        steps = []
        variables = list(expr.free_symbols)
        if variables:
            var = variables[0]
            steps.append(self._create_step(
                f"On factorise le trinôme du second degré en ${latex(var)}$"
            ))
            
            # Obtenir les coefficients
            try:
                poly = expr.as_poly(var)
                if poly:
                    coeffs = poly.all_coeffs()
                    if len(coeffs) >= 3:
                        a, b, c = coeffs[0], coeffs[1], coeffs[2]
                        steps.append(self._create_step(
                            f"Les coefficients sont : $a = {latex(a)}$, $b = {latex(b)}$, $c = {latex(c)}$"
                        ))
                        
                        # Calculer le discriminant
                        discriminant = b**2 - 4*a*c
                        discriminant_simplified = simplify(discriminant)
                        steps.append(self._create_step(
                            f"Discriminant : $\\Delta = b^2 - 4ac = {latex(discriminant_simplified)}$"
                        ))
                        
                        # Factoriser avec sympy
                        factored = factor(expr)
                        if factored != expr:
                            steps.append(self._create_step(
                                "Factorisation du trinôme",
                                f"${expr_latex} = {latex(factored)}$"
                            ))
                        else:
                            steps.append(self._create_step(
                                "Le trinôme ne peut pas être factorisé avec des nombres réels simples"
                            ))
            except:
                factored = factor(expr)
                steps.append(self._create_step(
                    "Factorisation directe",
                    f"${expr_latex} = {latex(factored)}$"
                ))
        
        return steps

    def _handle_common_factor(self, expr, expr_latex):
        """Gère la factorisation par facteur commun"""
        steps = []
        
        if isinstance(expr, Add):
            terms = expr.args
            # Calculer le GCD des termes
            terms_gcd = gcd(terms)
            
            if terms_gcd != 1 and terms_gcd != S.One:
                steps.append(self._create_step(
                    f"On identifie le facteur commun : ${latex(terms_gcd)}$"
                ))
                
                # Factoriser chaque terme
                factored_terms = []
                for term in terms:
                    quotient = simplify(term / terms_gcd)
                    factored_terms.append(quotient)
                
                factored_expr = Add(*factored_terms)
                steps.append(self._create_step(
                    "On factorise par le facteur commun",
                    f"${expr_latex} = {latex(terms_gcd)} \\times ({latex(factored_expr)})$"
                ))
                
                # Simplifier davantage si possible
                further_factored = factor(factored_expr)
                if further_factored != factored_expr:
                    final_result = terms_gcd * further_factored
                    steps.append(self._create_step(
                        "On factorise davantage l'expression entre parenthèses",
                        f"${expr_latex} = {latex(final_result)}$"
                    ))
        
        return steps

    def _handle_notable_identity(self, expr, expr_latex):
        """Gère les identités remarquables spéciales (cubes, etc.)"""
        steps = []
        
        if isinstance(expr, Add) and len(expr.args) == 2:
            a, b = expr.args
            # Somme de cubes a³ + b³
            if (isinstance(a, Pow) and a.exp == 3 and 
                isinstance(b, Pow) and b.exp == 3):
                if b.args[0] != -1:  # a³ + b³
                    steps.append(self._create_step(
                        "On reconnaît une somme de cubes : $a^3 + b^3 = (a + b)(a^2 - ab + b^2)$"
                    ))
                    
                    base_a = a.base
                    base_b = b.base
                    
                    steps.append(self._create_step(
                        f"On identifie : $a = {latex(base_a)}$ et $b = {latex(base_b)}$"
                    ))
                    
                    factored = factor(expr)
                    steps.append(self._create_step(
                        "On applique la formule de la somme de cubes",
                        f"${expr_latex} = {latex(factored)}$"
                    ))
                else:  # a³ - b³
                    steps.append(self._create_step(
                        "On reconnaît une différence de cubes : $a^3 - b^3 = (a - b)(a^2 + ab + b^2)$"
                    ))
                    
                    factored = factor(expr)
                    steps.append(self._create_step(
                        "On applique la formule de la différence de cubes",
                        f"${expr_latex} = {latex(factored)}$"
                    ))
        
        return steps

    def _handle_general_factorization(self, expr, expr_latex):
        """Gère la factorisation générale"""
        steps = []
        
        # Tenter la factorisation avec sympy
        factored = factor(expr)
        
        if factored != expr:
            steps.append(self._create_step(
                "On applique les techniques de factorisation",
                f"${expr_latex} = {latex(factored)}$"
            ))
            
            # Analyser le résultat pour donner plus d'explications
            if isinstance(factored, Mul):
                factors = factored.args
                if len(factors) > 1:
                    steps.append(self._create_step(
                        f"L'expression se factorise en {len(factors)} facteurs"
                    ))
        else:
            steps.append(self._create_step(
                "L'expression ne peut pas être factorisée davantage"
            ))
        
        return steps

    def _calculate_final_result(self, expr, expr_latex):
        """Calcule le résultat final factorisé"""
        factored = factor(expr)
        
        # Vérifier que la factorisation est correcte en développant
        expanded_check = expand(factored)
        original_expanded = expand(expr)
        
        if expanded_check.equals(original_expanded):
            self.steps.append(self._create_step(
                "Vérification : en développant le résultat, on retrouve bien l'expression initiale"
            ))
        
        return latex(factored)

    def _create_step(self, text=None, formula=None):
        """Crée une étape avec texte et/ou formule"""
        step = {}
        if text:
            step['text'] = text
        if formula:
            step['formula'] = formula
        return step 