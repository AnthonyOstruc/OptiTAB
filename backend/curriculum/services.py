from django.db import transaction
from .models import Theme, Notion, Exercice, MatiereContexte, ExerciceImage
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

    # Notions → (sheets) → Cours(+images), Quiz(+images), Exercices(+images)
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

        # Cours (one-to-one)
        cours = getattr(notion, 'cours', None)
        if cours:
            new_cours = Cours.objects.create(
                notion=new_notion,
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
        for quiz in notion.quiz.all().order_by('ordre', 'id'):
            new_quiz = Quiz.objects.create(
                notion=new_notion,
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
        for ex in notion.exercices.all().order_by('id'):
            new_ex = Exercice.objects.create(
                notion=new_notion,
                titre=ex.titre,
                contenu=ex.contenu,
                difficulty=ex.difficulty,
                est_actif=ex.est_actif,
                question=ex.question,
                reponse_correcte=ex.reponse_correcte,
                etapes=ex.etapes,
            )
            for eimg in ex.images.all().order_by('position', 'id'):
                ExerciceImage.objects.create(
                    exercice=new_ex,
                    image=eimg.image,
                    position=eimg.position,
                )

    return new_theme


@transaction.atomic
def duplicate_notion_deep(original: Notion, target_theme: Theme, new_title: str | None = None) -> Notion:
    """Clone une notion et tout son contenu (synthèse, chapitres, cours, quiz, exercices + images)
    vers un thème cible. Garantit un titre unique au sein du thème cible.

    Args:
        original: Notion d'origine à dupliquer
        target_theme: Thème cible dans lequel créer la copie
        new_title: Titre souhaité (optionnel). Si non fourni, reprend l'original et ajoute suffixe (Copie) si nécessaire

    Returns:
        La nouvelle instance de Notion clonée
    """
    base_title = (new_title or original.titre or 'Notion').strip()

    # Générer un titre unique dans le thème cible
    candidate = base_title
    index = 1
    while Notion.objects.filter(theme=target_theme, titre=candidate).exists():
        suffix = '' if index == 1 else f' {index}'
        candidate = f"{base_title} (Copie{suffix})"
        index += 1

    new_notion = Notion.objects.create(
        theme=target_theme,
        titre=candidate,
        description=original.description,
        couleur=original.couleur,
        svg_icon=original.svg_icon,
        ordre=original.ordre,
        est_actif=original.est_actif,
    )

    # Fiches de synthèse
    for sheet in original.synthesis_sheets.all().order_by('ordre', 'id'):
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

    # Cours (one-to-one)
    cours = getattr(original, 'cours', None)
    if cours:
        new_cours = Cours.objects.create(
            notion=new_notion,
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
    for quiz in original.quiz.all().order_by('ordre', 'id'):
        new_quiz = Quiz.objects.create(
            notion=new_notion,
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
    for ex in original.exercices.all().order_by('id'):
        new_ex = Exercice.objects.create(
            notion=new_notion,
            titre=ex.titre,
            contenu=ex.contenu,
            difficulty=ex.difficulty,
            est_actif=ex.est_actif,
            question=ex.question,
            reponse_correcte=ex.reponse_correcte,
            etapes=ex.etapes,
        )
        for eimg in ex.images.all().order_by('position', 'id'):
            ExerciceImage.objects.create(
                exercice=new_ex,
                image=eimg.image,
                position=eimg.position,
            )

    return new_notion

