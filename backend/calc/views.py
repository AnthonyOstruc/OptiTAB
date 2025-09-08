from rest_framework.views import APIView
from rest_framework.response import Response
from .derivative import DerivativeCalculator
from .integral import IntegralCalculator
from .expand import ExpandCalculator
from .factor import FactorCalculator
from .limit import LimitCalculator


class DerivativeView(APIView):
    """Vue pour calculer les dérivées avec étapes détaillées"""
    
    def __init__(self):
        super().__init__()
        self.calculator = DerivativeCalculator()

    def post(self, request):
        """Endpoint principal pour calculer la dérivée"""
        expr_latex = request.data.get('latex')
        if not expr_latex:
            return Response({'detail': 'latex missing'}, status=400)

        try:
            result = self.calculator.calculate_derivative(expr_latex)
            return Response(result)
        except Exception as e:
            return self._handle_error(e)

    def _handle_error(self, error):
        """Gère les erreurs de manière centralisée"""
        print(f"Erreur lors du calcul: {str(error)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return Response({'detail': f'Erreur lors du calcul: {str(error)}'}, status=400)


class IntegralView(APIView):
    """Vue pour calculer les intégrales avec étapes détaillées et pédagogiques"""
    
    def __init__(self):
        super().__init__()
        self.calculator = IntegralCalculator()

    def post(self, request):
        """Endpoint principal pour calculer l'intégrale"""
        expr_latex = request.data.get('latex')
        lower_bound = request.data.get('lower_bound')
        upper_bound = request.data.get('upper_bound')
        
        if not expr_latex:
            return Response({'detail': 'latex missing'}, status=400)

        try:
            result = self.calculator.calculate_integral(expr_latex, lower_bound, upper_bound)
            return Response(result)
        except Exception as e:
            return self._handle_error(e)

    def _handle_error(self, error):
        """Gère les erreurs de manière centralisée"""
        print(f"Erreur lors du calcul: {str(error)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return Response({'detail': f'Erreur lors du calcul: {str(error)}'}, status=400)


class ExpandView(APIView):
    """Vue pour développer les expressions algébriques avec étapes détaillées et pédagogiques"""
    
    def __init__(self):
        super().__init__()
        self.calculator = ExpandCalculator()

    def post(self, request):
        """Endpoint principal pour développer une expression"""
        expr_latex = request.data.get('latex')
        
        if not expr_latex:
            return Response({'detail': 'latex missing'}, status=400)

        try:
            result = self.calculator.calculate_expansion(expr_latex)
            return Response(result)
        except Exception as e:
            return self._handle_error(e)

    def _handle_error(self, error):
        """Gère les erreurs de manière centralisée"""
        print(f"Erreur lors du développement: {str(error)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return Response({'detail': f'Erreur lors du développement: {str(error)}'}, status=400)


class FactorView(APIView):
    """Vue pour factoriser les expressions algébriques avec étapes détaillées et pédagogiques"""
    
    def __init__(self):
        super().__init__()
        self.calculator = FactorCalculator()

    def post(self, request):
        """Endpoint principal pour factoriser une expression"""
        expr_latex = request.data.get('latex')
        
        if not expr_latex:
            return Response({'detail': 'latex missing'}, status=400)

        try:
            result = self.calculator.calculate_factorization(expr_latex)
            return Response(result)
        except Exception as e:
            return self._handle_error(e)

    def _handle_error(self, error):
        """Gère les erreurs de manière centralisée"""
        print(f"Erreur lors de la factorisation: {str(error)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return Response({'detail': f'Erreur lors de la factorisation: {str(error)}'}, status=400)


class LimitView(APIView):
    """Vue pour calculer les limites avec étapes détaillées et pédagogiques"""
    
    def __init__(self):
        super().__init__()
        self.calculator = LimitCalculator()

    def post(self, request):
        """Endpoint principal pour calculer une limite"""
        expr_latex = request.data.get('latex')
        limit_point = request.data.get('limit_point', None)  # Point vers lequel tend la variable
        direction = request.data.get('direction', None)      # 'left', 'right', ou None
        
        if not expr_latex:
            return Response({'detail': 'latex missing'}, status=400)

        try:
            result = self.calculator.calculate_limit(expr_latex, limit_point, direction)
            return Response(result)
        except Exception as e:
            return self._handle_error(e)

    def _handle_error(self, error):
        """Gère les erreurs de manière centralisée"""
        print(f"Erreur lors du calcul de limite: {str(error)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return Response({'detail': f'Erreur lors du calcul de limite: {str(error)}'}, status=400)
