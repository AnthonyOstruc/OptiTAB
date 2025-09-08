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
        """Développe une puissance d'une somme avec étapes détaillées"""
        steps = []
        
        base = expr.base
        n = expr.exp
        
        # Identifier les termes du binôme
        if isinstance(base, Add) and len(base.args) == 2:
            a, b = base.args
            
            # Étape 1: Identifier la structure
            steps.append(self._create_step(f"On développe la puissance : ${expr_latex}$"))
            
            # Étape 2: Afficher la formule du binôme de Newton
            if n <= 10:  # Pour les petites puissances, montrer la formule générale
                steps.append(self._create_step(
                    "On utilise la formule du binôme de Newton :",
                    f"$(a + b)^n = \\sum_{{k=0}}^{{n}} \\binom{{n}}{{k}} a^{{n-k}} b^k$"
                ))
                
                # Étape 3: Application de la formule avec les valeurs spécifiques
                steps.append(self._create_step(
                    f"Pour $a = {latex(a)}$, $b = {latex(b)}$ et $n = {n}$ :",
                    f"$({latex(a)} + {latex(b)})^{{{n}}} = \\sum_{{k=0}}^{{{n}}} \\binom{{{n}}}{{k}} ({latex(a)})^{{{n}-k}} ({latex(b)})^k$"
                ))
                
                # Étape 4: Développement terme par terme
                if n <= 6:  # Pour les petites puissances, montrer quelques termes
                    self._show_binomial_terms(steps, a, b, n)
                elif n <= 10:  # Pour les puissances moyennes, montrer les premiers termes
                    self._show_first_binomial_terms(steps, a, b, n)
            else:
                # Pour les grandes puissances, juste mentionner la formule
                steps.append(self._create_step(
                    "On utilise la formule du binôme de Newton pour développer cette puissance élevée :",
                    f"$(a + b)^{{{n}}} = \\sum_{{k=0}}^{{{n}}} \\binom{{{n}}}{{k}} a^{{{n}-k}} b^k$"
                ))
        
        # Calcul final
        expanded = expand(expr)
        steps.append(self._create_step(
            "Résultat du développement :",
            f"${expr_latex} = {latex(expanded)}$"
        ))
        
        return steps

    def _show_binomial_terms(self, steps, a, b, n):
        """Affiche les termes du développement binomial un par un de manière pédagogique"""
        from sympy import binomial
        
        # Étape 1: Montrer tous les termes avec la formule générale
        terms_formula = []
        for k in range(n + 1):
            term_str = f"\\binom{{{n}}}{{{k}}}"
            
            a_power = n - k
            b_power = k
            
            if a_power > 0:
                if a_power == 1:
                    term_str += f"({latex(a)})"
                else:
                    term_str += f"({latex(a)})^{{{a_power}}}"
            
            if b_power > 0:
                if b_power == 1:
                    term_str += f"({latex(b)})"
                else:
                    term_str += f"({latex(b)})^{{{b_power}}}"
            
            if a_power == 0 and b_power == 0:
                term_str += "1"
                
            terms_formula.append(term_str)
        
        formula_expanded = " + ".join(terms_formula)
        steps.append(self._create_step(
            f"Développement complet avec tous les termes :",
            f"$({latex(a)} + {latex(b)})^{{{n}}} = {formula_expanded}$"
        ))
        
        # Étape 2: Calculer chaque coefficient binomial séparément
        coeff_calculations = []
        for k in range(n + 1):
            coeff = int(binomial(n, k))
            coeff_calculations.append(f"$\\binom{{{n}}}{{{k}}} = {coeff}$")
        
        steps.append(self._create_step(
            "Calcul des coefficients binomiaux :",
            ", ".join(coeff_calculations)
        ))
        
        # Étape 3: Remplacer les coefficients et calculer chaque terme
        term_calculations = []
        final_terms = []
        
        for k in range(n + 1):
            coeff = int(binomial(n, k))
            a_power = n - k
            b_power = k
            
            # Construire la partie avec coefficient binomial
            term_with_binom = f"\\binom{{{n}}}{{{k}}}"
            if a_power > 0:
                if a_power == 1:
                    term_with_binom += f"({latex(a)})"
                else:
                    term_with_binom += f"({latex(a)})^{{{a_power}}}"
            
            if b_power > 0:
                if b_power == 1:
                    term_with_binom += f"({latex(b)})"
                else:
                    term_with_binom += f"({latex(b)})^{{{b_power}}}"
            
            # Calculer les valeurs
            a_val = expand(a**a_power) if a_power > 0 else 1
            b_val = expand(b**b_power) if b_power > 0 else 1
            term_value = expand(coeff * a_val * b_val)
            
            # Formatage aligné avec indentation visuelle cohérente
            calculation_line = f"$\\qquad {term_with_binom} = {coeff} \\times {latex(a_val)} \\times {latex(b_val)} = {latex(term_value)}$"
            
            term_calculations.append(calculation_line)
            final_terms.append(latex(term_value))
        
        steps.append(self._create_step(
            "Calcul de chaque terme :",
            "\\\\".join(term_calculations)
        ))
        
        # Étape 4: Résultat final
        final_result = " + ".join(final_terms)
        steps.append(self._create_step(
            "Assemblage du résultat final :",
            f"$({latex(a)} + {latex(b)})^{{{n}}} = {final_result}$"
        ))

    def _show_first_binomial_terms(self, steps, a, b, n):
        """Affiche les premiers termes du développement binomial pour les puissances moyennes"""
        from sympy import binomial
        
        # Montrer les 4 premiers et 2 derniers termes
        terms_to_show = []
        
        # Premiers termes
        for k in range(min(3, n + 1)):
            coeff = int(binomial(n, k))
            a_power = n - k
            b_power = k
            
            term_latex = self._format_binomial_term(a, b, coeff, a_power, b_power)
            actual_value = expand(coeff * (a**a_power if a_power > 0 else 1) * (b**b_power if b_power > 0 else 1))
            
            terms_to_show.append(f"$\\binom{{{n}}}{{{k}}} = {coeff}$ → ${latex(actual_value)}$")
        
        if n > 6:
            terms_to_show.append("$\\ldots$")
            
            # Derniers termes
            for k in range(max(3, n - 1), n + 1):
                coeff = int(binomial(n, k))
                a_power = n - k
                b_power = k
                
                actual_value = expand(coeff * (a**a_power if a_power > 0 else 1) * (b**b_power if b_power > 0 else 1))
                terms_to_show.append(f"$\\binom{{{n}}}{{{k}}} = {coeff}$ → ${latex(actual_value)}$")
        
        steps.append(self._create_step(
            f"Exemples de termes du développement :",
            ", ".join(terms_to_show)
        ))

    def _format_binomial_term(self, a, b, coeff, a_power, b_power):
        """Formate un terme binomial"""
        term_str = ""
        if coeff != 1:
            term_str += str(coeff)
        
        if a_power > 0:
            if a_power == 1:
                term_str += f"({latex(a)})"
            else:
                term_str += f"({latex(a)})^{{{a_power}}}"
        
        if b_power > 0:
            if b_power == 1:
                term_str += f"({latex(b)})"
            else:
                term_str += f"({latex(b)})^{{{b_power}}}"
        
        return term_str

    def _handle_general_expansion(self, expr, expr_latex):
        """Développe une expression complexe avec étapes détaillées"""
        steps = []
        
        # Analyser la structure de l'expression
        steps.append(self._create_step(f"Développement de l'expression complexe : ${expr_latex}$"))
        
        # Identifier les différents types de termes
        if isinstance(expr, Add):
            # Expression est une somme de termes
            terms = expr.args
            self._analyze_sum_terms(steps, terms, expr_latex)
        else:
            # Expression est autre chose, utiliser la méthode générale
            steps.append(self._create_step("Application du développement général"))
            expanded = expand(expr)
            steps.append(self._create_step("Résultat développé", f"${latex(expanded)}$"))
        
        return steps

    def _analyze_sum_terms(self, steps, terms, expr_latex):
        """Analyse chaque terme d'une somme et les développe séparément"""
        steps.append(self._create_step(
            f"L'expression est une somme de {len(terms)} termes :",
            f"${expr_latex} = " + " + ".join([f"({latex(term)})" for term in terms]) + "$"
        ))
        
        # Identifier et développer chaque terme
        expanded_terms = []
        needs_expansion = []
        
        for i, term in enumerate(terms, 1):
            if self._term_needs_expansion(term):
                needs_expansion.append((i, term))
                
        if needs_expansion:
            steps.append(self._create_step(
                f"Termes nécessitant un développement :",
                ", ".join([f"Terme {i}: $({latex(term)})$" for i, term in needs_expansion])
            ))
            
            # Développer chaque terme complexe
            for i, term in needs_expansion:
                self._expand_individual_term(steps, term, i)
        
        # Calculer le résultat final
        total_expanded = expand(sum(terms))
        steps.append(self._create_step(
            "Développement complet et simplification :",
            f"${expr_latex} = {latex(total_expanded)}$"
        ))

    def _term_needs_expansion(self, term):
        """Détermine si un terme a besoin d'être développé"""
        # Puissances de binômes
        if isinstance(term, Pow) and isinstance(term.base, Add):
            return True
        # Produits de polynômes
        elif isinstance(term, Mul) and any(isinstance(arg, Add) for arg in term.args):
            return True
        # Expressions imbriquées
        elif isinstance(term, Add) and any(self._term_needs_expansion(subterm) for subterm in term.args):
            return True
        return False

    def _expand_individual_term(self, steps, term, term_number):
        """Développe un terme individuel avec détails"""
        if isinstance(term, Pow) and isinstance(term.base, Add):
            # C'est une puissance d'un binôme
            base = term.base
            exp = term.exp
            
            if len(base.args) == 2 and exp <= 5:
                # Développement binomial détaillé
                a, b = base.args
                
                # Étape 1: Identifier les valeurs a et b avec formatage LaTeX propre
                steps.append(self._create_step(
                    f"Développement du terme {term_number} avec le binôme de Newton :",
                    f"$({latex(base)})^{{{exp}}}$ avec $a = {latex(a)}$ et $b = {latex(b)}$"
                ))
                
                # Étape 2: Rappeler la formule du binôme
                steps.append(self._create_step(
                    "Formule du binôme de Newton :",
                    f"$(a + b)^{{{exp}}} = \\sum_{{k=0}}^{{{exp}}} \\binom{{{exp}}}{{k}} a^{{{exp}-k}} b^k$"
                ))
                
                # Utiliser la formule du binôme
                from sympy import binomial
                binomial_terms = []
                for k in range(exp + 1):
                    coeff = int(binomial(exp, k))
                    a_power = exp - k
                    b_power = k
                    
                    a_val = expand(a**a_power) if a_power > 0 else 1
                    b_val = expand(b**b_power) if b_power > 0 else 1
                    term_value = expand(coeff * a_val * b_val)
                    
                    binomial_terms.append(latex(term_value))
                
                result = " + ".join(binomial_terms)
                steps.append(self._create_step(
                    f"Résultat du développement du terme {term_number} :",
                    f"$({latex(base)})^{{{exp}}} = {result}$"
                ))
            else:
                # Développement simple
                expanded_term = expand(term)
                steps.append(self._create_step(
                    f"Développement du terme {term_number} :",
                    f"$({latex(term)}) = {latex(expanded_term)}$"
                ))
        else:
            # Autre type de terme
            expanded_term = expand(term)
            steps.append(self._create_step(
                f"Développement du terme {term_number} :",
                f"$({latex(term)}) = {latex(expanded_term)}$"
            ))

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
