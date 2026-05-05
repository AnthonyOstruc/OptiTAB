"""
Seed the Arena game with starter chapters / levels / questions.

Usage:
    python manage.py seed_arena

Idempotent: running it twice will not duplicate content.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from mathgame.models import (
    ArenaChapter,
    ArenaConfig,
    ArenaDailyChallenge,
    ArenaLevel,
    ArenaQuestion,
)


SEED = [
    {
        'title': 'Calcul mental express',
        'slug': 'calcul-mental-express',
        'description': "Sharpen your speed: addition, soustraction, multiplication.",
        'icon': '⚡',
        'color': '#2563eb',
        'order': 1,
        'is_premium': False,
        'levels': [
            {
                'order': 1, 'title': 'Échauffement', 'difficulty': 'easy', 'is_premium': False,
                'time_limit_sec': 90, 'xp_reward': 20, 'pass_threshold': 60,
                'questions': [
                    {'prompt': r"Combien font $7 \times 8$ ?", 'choices': ['54', '56', '58', '64'], 'correct': [1],
                     'explanation': "Table de 7: 7 × 8 = 56."},
                    {'prompt': r"$15 + 27 = ?$", 'choices': ['41', '42', '43', '52'], 'correct': [1],
                     'explanation': "15 + 27 = 42 (15 + 25 = 40, +2)."},
                    {'prompt': r"$144 \div 12 = ?$", 'choices': ['10', '11', '12', '14'], 'correct': [2],
                     'explanation': "12 × 12 = 144."},
                    {'prompt': r"$9 \times 6 = ?$", 'choices': ['52', '54', '56', '58'], 'correct': [1],
                     'explanation': "9 × 6 = 54."},
                    {'prompt': r"$100 - 37 = ?$", 'choices': ['53', '63', '67', '73'], 'correct': [1],
                     'explanation': "100 - 37 = 63."},
                ],
            },
            {
                'order': 2, 'title': 'Vitesse pure', 'difficulty': 'medium', 'is_premium': False,
                'time_limit_sec': 75, 'xp_reward': 30, 'pass_threshold': 70,
                'questions': [
                    {'prompt': r"$13 \times 7 = ?$", 'choices': ['81', '91', '93', '101'], 'correct': [1],
                     'explanation': "13 × 7 = 91 (10×7 + 3×7)."},
                    {'prompt': r"$256 \div 8 = ?$", 'choices': ['28', '30', '32', '36'], 'correct': [2],
                     'explanation': "8 × 32 = 256."},
                    {'prompt': r"$48 + 67 = ?$", 'choices': ['105', '115', '125', '135'], 'correct': [1],
                     'explanation': "48 + 67 = 115."},
                    {'prompt': r"$9^2 = ?$", 'choices': ['72', '79', '81', '99'], 'correct': [2],
                     'explanation': "9² = 81."},
                    {'prompt': r"$\sqrt{144} = ?$", 'choices': ['10', '11', '12', '14'], 'correct': [2],
                     'explanation': "12 × 12 = 144 donc √144 = 12."},
                ],
            },
            {
                'order': 3, 'title': 'Calcul tactique', 'difficulty': 'medium', 'is_premium': True,
                'time_limit_sec': 60, 'xp_reward': 45, 'pass_threshold': 70,
                'questions': [
                    {'prompt': r"$25 \times 32 = ?$", 'choices': ['600', '700', '800', '900'], 'correct': [2],
                     'explanation': "25 × 32 = 25 × 4 × 8 = 100 × 8 = 800."},
                    {'prompt': r"$17 \times 23 = ?$", 'choices': ['381', '391', '401', '411'], 'correct': [1],
                     'explanation': "17 × 23 = 17 × 20 + 17 × 3 = 340 + 51 = 391."},
                    {'prompt': r"$5\% \text{ de } 240 = ?$", 'choices': ['10', '12', '14', '24'], 'correct': [1],
                     'explanation': "5% = 1/20 ; 240 / 20 = 12."},
                    {'prompt': r"$\frac{3}{4} + \frac{2}{3} = ?$", 'choices': ['5/7', '17/12', '5/12', '11/12'], 'correct': [1],
                     'explanation': "Mise au même dénominateur: 9/12 + 8/12 = 17/12."},
                    {'prompt': r"$2^{10} = ?$", 'choices': ['512', '1000', '1024', '2048'], 'correct': [2],
                     'explanation': "2^10 = 1024."},
                ],
            },
        ],
    },
    {
        'title': 'Fonctions affines',
        'slug': 'fonctions-affines',
        'description': "Lectures graphiques, équations $y=ax+b$.",
        'icon': '📈',
        'color': '#7c3aed',
        'order': 2,
        'is_premium': False,
        'levels': [
            {
                'order': 1, 'title': 'Reconnaître $y=ax+b$', 'difficulty': 'easy', 'is_premium': False,
                'time_limit_sec': 120, 'xp_reward': 25, 'pass_threshold': 60,
                'questions': [
                    {'prompt': r"$f(x) = 2x + 3$. Quelle est l'image de $4$ ?",
                     'choices': ['8', '9', '10', '11'], 'correct': [3],
                     'explanation': "f(4) = 2×4 + 3 = 11."},
                    {'prompt': r"Le coefficient directeur de $y = -3x + 5$ est :",
                     'choices': ['5', '-3', '3', '-5'], 'correct': [1],
                     'explanation': "Dans y=ax+b, a est le coefficient directeur, ici a=-3."},
                    {'prompt': r"L'ordonnée à l'origine de $y = \frac{1}{2}x - 4$ est :",
                     'choices': ['1/2', '-4', '4', '-1/2'], 'correct': [1],
                     'explanation': "C'est la valeur de b, ici -4."},
                    {'prompt': r"$f(x)=ax+b$ et $f(0)=2$, $f(1)=5$. Alors $a$ vaut :",
                     'choices': ['2', '3', '5', '7'], 'correct': [1],
                     'explanation': "f(1)-f(0) = a = 5-2 = 3."},
                    {'prompt': r"La fonction $f(x)=2x$ est :",
                     'choices': ['affine non linéaire', 'linéaire', 'constante', 'aucune'], 'correct': [1],
                     'explanation': "Pas de constante b, donc linéaire (cas particulier d'affine)."},
                ],
            },
            {
                'order': 2, 'title': "Équations $ax+b=0$", 'difficulty': 'medium', 'is_premium': False,
                'time_limit_sec': 120, 'xp_reward': 30, 'pass_threshold': 60,
                'questions': [
                    {'prompt': r"Résoudre $2x+6=0$.",
                     'choices': ['x=3', 'x=-3', 'x=6', 'x=-6'], 'correct': [1],
                     'explanation': "2x = -6 donc x = -3."},
                    {'prompt': r"Résoudre $3x-12=0$.",
                     'choices': ['x=-4', 'x=4', 'x=12', 'x=-12'], 'correct': [1],
                     'explanation': "3x = 12 donc x = 4."},
                    {'prompt': r"Résoudre $-x+5=0$.",
                     'choices': ['x=-5', 'x=5', 'x=0', 'x=1'], 'correct': [1],
                     'explanation': "-x = -5 donc x = 5."},
                    {'prompt': r"Résoudre $5x = 2x + 9$.",
                     'choices': ['x=1', 'x=2', 'x=3', 'x=4'], 'correct': [2],
                     'explanation': "3x = 9 donc x = 3."},
                    {'prompt': r"Résoudre $\frac{x}{2}+1=4$.",
                     'choices': ['x=3', 'x=5', 'x=6', 'x=8'], 'correct': [2],
                     'explanation': "x/2 = 3 donc x = 6."},
                ],
            },
            {
                'order': 3, 'title': 'Lecture graphique élite', 'difficulty': 'hard', 'is_premium': True,
                'time_limit_sec': 120, 'xp_reward': 60, 'pass_threshold': 70,
                'questions': [
                    {'prompt': r"Une droite passe par $(1,2)$ et $(3,8)$. Coefficient directeur :",
                     'choices': ['2', '3', '4', '6'], 'correct': [1],
                     'explanation': "(8-2)/(3-1) = 6/2 = 3."},
                    {'prompt': r"$y=ax+b$ passe par $(0,4)$ et $(2,0)$. $f(x)$ ?",
                     'choices': ['$y=2x+4$', '$y=-2x+4$', '$y=-x+4$', '$y=2x-4$'], 'correct': [1],
                     'explanation': "a=(0-4)/(2-0)=-2 ; b=4."},
                    {'prompt': r"Pour quel $x$ a-t-on $-x+5=2x-1$ ?",
                     'choices': ['x=1', 'x=2', 'x=3', 'x=4'], 'correct': [1],
                     'explanation': "5+1 = 3x donc x=2."},
                    {'prompt': r"La droite $y=-3x+1$ est :",
                     'choices': ['croissante', 'décroissante', 'constante', 'verticale'], 'correct': [1],
                     'explanation': "a<0 → fonction affine décroissante."},
                    {'prompt': r"Soit $f(x)=ax+b$. $f(2)=7$ et $f(5)=1$. $a$ ?",
                     'choices': ['2', '-2', '3', '-3'], 'correct': [1],
                     'explanation': "(1-7)/(5-2) = -6/3 = -2."},
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Seed Arena game data (idempotent)."

    @transaction.atomic
    def handle(self, *args, **options):
        config = ArenaConfig.get_solo()
        self.stdout.write(self.style.NOTICE(
            f"Arena config (is_public={config.is_public}, version={config.version})"
        ))

        for chapter_data in SEED:
            chapter, _ = ArenaChapter.objects.update_or_create(
                slug=chapter_data['slug'],
                defaults={
                    'title': chapter_data['title'],
                    'description': chapter_data['description'],
                    'icon': chapter_data['icon'],
                    'color': chapter_data['color'],
                    'order': chapter_data['order'],
                    'is_premium': chapter_data['is_premium'],
                    'is_active': True,
                },
            )
            for level_data in chapter_data['levels']:
                level, _ = ArenaLevel.objects.update_or_create(
                    chapter=chapter, order=level_data['order'],
                    defaults={
                        'title': level_data['title'],
                        'difficulty': level_data['difficulty'],
                        'time_limit_sec': level_data['time_limit_sec'],
                        'xp_reward': level_data['xp_reward'],
                        'pass_threshold': level_data['pass_threshold'],
                        'is_premium': level_data['is_premium'],
                        'is_active': True,
                    },
                )
                for index, q_data in enumerate(level_data['questions'], start=1):
                    ArenaQuestion.objects.update_or_create(
                        level=level, order=index,
                        defaults={
                            'type': 'mcq',
                            'prompt': q_data['prompt'],
                            'choices': q_data['choices'],
                            'correct': q_data['correct'],
                            'explanation': q_data.get('explanation', ''),
                            'hint': q_data.get('hint', ''),
                            'weight': 1,
                        },
                    )

        # Make today's daily = first level of first chapter.
        first_level = ArenaLevel.objects.order_by('chapter__order', 'order').first()
        if first_level:
            ArenaDailyChallenge.objects.update_or_create(
                date=timezone.localdate(),
                defaults={'level': first_level, 'bonus_xp': 50},
            )
        self.stdout.write(self.style.SUCCESS("Arena content seeded."))
