from rest_framework import serializers


class MathRunScoreSubmitSerializer(serializers.Serializer):
    score = serializers.IntegerField(min_value=0, max_value=9999)
    category = serializers.ChoiceField(
        choices=[
            'all', 'addition', 'subtraction', 'multiplication', 'division',
            'limits', 'derivatives', 'integrals', 'sequences',
        ],
        default='all',
    )
