from django.db import transaction
from .models import Theme, Notion, Chapitre, Exercice, MatiereContexte, ExerciceImage
from cours.models import Cours, CoursImage
from quiz.models import Quiz, QuizImage
from synthesis.models import SynthesisSheet


def _generate_unique_title(base_title: str, target_contexte: MatiereContexte) -> str:
    base = base_title or 'Thème'
    candidate = base
    index = 1
    while Theme.objects.filter(contexte=target_contexte, titre=candidate).exists():
        suffix = '' if index == 1 else f' {index}'
        candidate = f"{base} (Copie{suffix})"
        index += 1
    return candidate


@transaction.atomic
def duplicate_theme_deep(original: Theme, target_contexte: MatiereContexte, new_title: str | None = None) -> Theme:
    """Clone un thème et tout son contenu vers un contexte cible.

    - Conserve l'ordre, la difficulté, le contenu, les images, etc.
    - Garantit un titre unique dans le contexte cible.
    """
    unique_title = _generate_unique_title((new_title or original.titre or 'Thème').strip(), target_contexte)

    # Créer le nouveau thème
    new_theme = Theme.objects.create(
        titre=unique_title,
        matiere=target_contexte.matiere,
        contexte=target_contexte,
        description=original.description,
        couleur=original.couleur,
        svg_icon=original.svg_icon,
        ordre=original.ordre,
        est_actif=original.est_actif,
    )

    # Notions → (sheets) → Chapitres → Cours(+images), Quiz(+images), Exercices(+images)
    for notion in original.notions.all().order_by('ordre', 'id'):
        new_notion = Notion.objects.create(
            theme=new_theme,
            titre=notion.titre,
            description=notion.description,
            couleur=notion.couleur,
            svg_icon=notion.svg_icon,
            ordre=notion.ordre,
            est_actif=notion.est_actif,
        )

        # Fiches de synthèse
        for sheet in notion.synthesis_sheets.all().order_by('ordre', 'id'):
            SynthesisSheet.objects.create(
                notion=new_notion,
                titre=sheet.titre,
                summary=sheet.summary,
                key_points=sheet.key_points,
                formulas=sheet.formulas,
                examples=sheet.examples,
                difficulty=sheet.difficulty,
                ordre=sheet.ordre,
                est_actif=sheet.est_actif,
                reading_time_minutes=sheet.reading_time_minutes,
            )

        for chapitre in notion.chapitres.all().order_by('ordre', 'id'):
            new_chapitre = Chapitre.objects.create(
                notion=new_notion,
                titre=chapitre.titre,
                contenu=chapitre.contenu,
                difficulty=chapitre.difficulty,
                ordre=chapitre.ordre,
                est_actif=chapitre.est_actif,
            )

            # Cours (one-to-one)
            cours = getattr(chapitre, 'cours', None)
            if cours:
                new_cours = Cours.objects.create(
                    chapitre=new_chapitre,
                    titre=cours.titre,
                    contenu=cours.contenu,
                    difficulty=cours.difficulty,
                    ordre=cours.ordre,
                    est_actif=cours.est_actif,
                    video_url=cours.video_url,
                )
                for img in cours.images.all().order_by('position', 'id'):
                    CoursImage.objects.create(
                        cours=new_cours,
                        image=img.image,
                        image_type=img.image_type,
                        position=img.position,
                        legende=img.legende,
                    )

            # Quiz
            for quiz in chapitre.quiz.all().order_by('ordre', 'id'):
                new_quiz = Quiz.objects.create(
                    chapitre=new_chapitre,
                    titre=quiz.titre,
                    contenu=quiz.contenu,
                    difficulty=quiz.difficulty,
                    ordre=quiz.ordre,
                    est_actif=quiz.est_actif,
                    questions_data=quiz.questions_data,
                    duree_minutes=quiz.duree_minutes,
                )
                for qimg in quiz.images.all().order_by('position', 'id'):
                    QuizImage.objects.create(
                        quiz=new_quiz,
                        image=qimg.image,
                        image_type=qimg.image_type,
                        position=qimg.position,
                        legende=qimg.legende,
                    )

            # Exercices
            for ex in chapitre.exercices.all().order_by('ordre', 'id'):
                new_ex = Exercice.objects.create(
                    chapitre=new_chapitre,
                    titre=ex.titre,
                    contenu=ex.contenu,
                    difficulty=ex.difficulty,
                    ordre=ex.ordre,
                    est_actif=ex.est_actif,
                    question=ex.question,
                    reponse_correcte=ex.reponse_correcte,
                    etapes=ex.etapes,
                    points=ex.points,
                )
                for eimg in ex.images.all().order_by('position', 'id'):
                    ExerciceImage.objects.create(
                        exercice=new_ex,
                        image=eimg.image,
                        image_type=eimg.image_type,
                        position=eimg.position,
                        legende=eimg.legende,
                    )

    return new_theme


