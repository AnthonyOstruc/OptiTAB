from __future__ import annotations

from types import SimpleNamespace

from django.test import SimpleTestCase

from cours.services.pdf import _extract_metadata_and_body, build_course_pdf_filename


class CoursePdfServiceTests(SimpleTestCase):
    def test_extract_metadata_and_body_renders_annale_blocks(self) -> None:
        source = """
=== [Annale - Calcul litteral]
Difficulte: hard
Niveau: Premiere
Matiere: Mathematiques
Type: DS
Duree: 60 min
Points: 20
Ordre: 2
Description: Sujet type bac

Consigne: Simplifier les expressions.
Questions:
1. Simplifier A = 3x + 5x - 7.
2. Simplifier B = 2(x - 3) - 4(x + 2).

Etapes:
- Reperer la methode.
- Calculer proprement.

Correction_detaillee:
1. A = 8x - 7.
2. B = -2x - 14.

Reponses_finales:
1. A = 8x - 7
2. B = -2x - 14

Bareme:
- Q1: 10 pts
- Q2: 10 pts
===

=== [Annale - Suites]
Difficulte: medium
Enonce: Etudier la suite u_n.
Question 1: Calculer u_4.
Solution: u_4 = 17.
===
"""
        metadata, body = _extract_metadata_and_body(source)

        self.assertEqual(metadata.get("title"), "Annale - Calcul litteral")
        self.assertEqual(metadata.get("exercise_count"), "2")
        self.assertIn("annale-card", body)
        self.assertIn("annale-section--questions", body)
        self.assertIn("annale-section--correction", body)
        self.assertIn("annale-section--final", body)
        self.assertIn("annale-badge--type", body)
        self.assertIn("annale-badge--duree", body)

    def test_extract_metadata_and_body_keeps_simple_plain_text(self) -> None:
        source = """
Titre: Rappels d algebre
Description: Revision rapide

Une expression litterale contient des lettres.

On peut reduire les termes semblables.
"""
        metadata, body = _extract_metadata_and_body(source)

        self.assertEqual(metadata.get("title"), "Rappels d algebre")
        self.assertEqual(metadata.get("description"), "Revision rapide")
        self.assertIn("<p>", body)
        self.assertNotIn("annale-card", body)
        self.assertNotIn("Titre:", body)

    def test_build_course_pdf_filename_uses_parsed_title(self) -> None:
        course = SimpleNamespace(
            titre="",
            contenu="""
=== [Annale - Fonctions]
Difficulte: medium
Enonce: Calculer une image.
===
""",
            notion=None,
            pk=42,
        )

        filename = build_course_pdf_filename(course)
        self.assertEqual(filename, "annale-fonctions.pdf")

    def test_extract_metadata_and_body_handles_inline_figure_blocks(self) -> None:
        source = """
=== [Annale - Derivation]
Difficulte: medium
Enonce: Lire la pente d une tangente.
<figure><img src="data:image/png;base64,AAAA" alt="schema" /></figure>
Question 1: Determiner f'(2).

Etapes:
- Lire deux points de la tangente.

Solution:
1. f'(2) = 3.
===
"""
        metadata, body = _extract_metadata_and_body(source)

        self.assertEqual(metadata.get("title"), "Annale - Derivation")
        self.assertIn("annale-card", body)
        self.assertIn("annale-question", body)
        self.assertIn("<figure>", body)
        self.assertNotIn("[[HTML_BLOCK_", body)

    def test_extract_metadata_and_body_supports_master_pedagogical_sections(self) -> None:
        source = """
=== [Template Maitre]
Titre: Exercice derivee
Niveau: Premiere
Matiere: Mathematiques
Chapitre: Derivation
Notion: Nombre derive
Type d exercice: application
Temps estime: 15 min
Objectif pedagogique principal: Lire une pente.
Prerequis: Coefficient directeur
Erreurs frequentes: Inversion de soustraction

[OBJECTIF]
Comprendre la pente.

[PREREQUIS]
- Coefficient directeur

[ENONCE]
Donner f'(-1) et f'(2).

Questions:
1. Calculer f'(-1).
2. Calculer f'(2).

[A RETENIR]
- Le nombre derive est une pente.
===
"""
        metadata, body = _extract_metadata_and_body(source)

        self.assertEqual(metadata.get("title"), "Exercice derivee")
        self.assertEqual(metadata.get("duree"), "15 min")
        self.assertEqual(metadata.get("type"), "application")
        self.assertIn("annale-card", body)
        self.assertIn("annale-section--questions", body)
        self.assertIn("annale-section--final", body)
