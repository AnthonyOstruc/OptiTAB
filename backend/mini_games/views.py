from django.db.models import Max
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import MathRunScore
from .permissions import IsStaffOrSuperuser
from .serializers import MathRunScoreSubmitSerializer
from users.models import CustomUser


@api_view(['POST'])
@permission_classes([IsStaffOrSuperuser])
def submit_score(request):
    serializer = MathRunScoreSubmitSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    score = serializer.validated_data['score']
    category = serializer.validated_data['category']
    user = request.user

    existing_best = (
        MathRunScore.objects
        .filter(user=user, category=category)
        .aggregate(best=Max('score'))['best'] or 0
    )
    is_new_record = score > existing_best

    if is_new_record:
        MathRunScore.objects.create(user=user, score=score, category=category)

    return Response({
        'score': score,
        'category': category,
        'is_new_record': is_new_record,
        'best_score': max(score, existing_best),
    })


@api_view(['GET'])
@permission_classes([IsStaffOrSuperuser])
def get_leaderboard(request):
    category = request.query_params.get('category', 'all')
    if category not in ['all', 'addition', 'subtraction', 'multiplication', 'division']:
        category = 'all'
    limit = min(int(request.query_params.get('limit', 10)), 50)

    top = (
        MathRunScore.objects
        .filter(category=category)
        .values('user')
        .annotate(score=Max('score'))
        .order_by('-score')[:limit]
    )

    me_id = getattr(request.user, 'id', None)
    results = []
    for i, entry in enumerate(top, 1):
        try:
            u = CustomUser.objects.only('id', 'first_name').get(pk=entry['user'])
            results.append({
                'rank': i,
                'user_id': u.id,
                'first_name': u.first_name,
                'score': entry['score'],
                'is_me': u.id == me_id,
            })
        except CustomUser.DoesNotExist:
            pass

    return Response({'category': category, 'leaderboard': results})
