from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import logging
logger = logging.getLogger(__name__)
from rest_framework.response import Response
from .derivative import DerivativeCalculator
from .integral import IntegralCalculator
from .expand import ExpandCalculator
from .factor import FactorCalculator
from .limit import LimitCalculator


class BaseCalcView(APIView):
    """Base view for calculator endpoints with public access and gated steps output."""

    permission_classes = [AllowAny]

    def format_response(self, result: dict, request) -> Response:
        """
        Return full result (with steps) for authenticated users.
        For anonymous users, return only the final result without steps.
        """
        try:
            is_auth = bool(getattr(request, "user", None) and request.user.is_authenticated)
        except Exception:
            is_auth = False

        if is_auth:
            return Response(result)

        # Anonymous: only expose final result, hide steps for free tier
        return Response({
            'result_latex': result.get('result_latex'),
            'steps': []
        })

    def error_response(self, error: Exception, message: str) -> Response:
        import traceback
        logger.error(f"{message}: {str(error)}\n{traceback.format_exc()}")
        return Response({'detail': f'{message}: {str(error)}'}, status=400)


class DerivativeView(BaseCalcView):
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
            return self.format_response(result, request)
        except Exception as e:
            return self.error_response(e, "Erreur lors du calcul")


class IntegralView(BaseCalcView):
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
            return self.format_response(result, request)
        except Exception as e:
            return self.error_response(e, "Erreur lors du calcul")


class ExpandView(BaseCalcView):
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
            return self.format_response(result, request)
        except Exception as e:
            return self.error_response(e, "Erreur lors du développement")


class FactorView(BaseCalcView):
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
            return self.format_response(result, request)
        except Exception as e:
            return self.error_response(e, "Erreur lors de la factorisation")


class LimitView(BaseCalcView):
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
            return self.format_response(result, request)
        except Exception as e:
            return self.error_response(e, "Erreur lors du calcul de limite")
