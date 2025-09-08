#!/usr/bin/env python
"""
Script de nettoyage des variables d'environnement proxy pour OpenAI
"""
import os
import sys

def clean_proxy_environment():
    """Nettoie les variables d'environnement proxy problématiques"""
    print("🧹 Nettoyage des variables d'environnement proxy")
    print("=" * 50)

    proxy_vars = [
        'HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy',
        'OPENAI_PROXY', 'REQUESTS_CA_BUNDLE', 'SSL_CERT_FILE',
        'ALL_PROXY', 'all_proxy', 'no_proxy', 'NO_PROXY'
    ]

    cleaned_vars = []

    for var in proxy_vars:
        if var in os.environ:
            del os.environ[var]
            cleaned_vars.append(var)
            print(f"✅ Supprimé: {var}")
        else:
            print(f"ℹ️  Non défini: {var}")

    if cleaned_vars:
        print(f"\n🎉 {len(cleaned_vars)} variables proxy nettoyées")
    else:
        print("\nℹ️  Aucune variable proxy trouvée")

    # Nettoyer aussi les variables système
    print("\n🔧 Nettoyage des configurations système")
    print("-" * 40)

    # Désactiver urllib3 warnings
    os.environ['PYTHONWARNINGS'] = 'ignore'

    # Nettoyer les configurations OpenSSL problématiques
    openssl_vars = ['OPENSSL_CONF', 'SSL_CERT_DIR', 'SSL_CERT_FILE']
    for var in openssl_vars:
        if var in os.environ:
            del os.environ[var]
            print(f"✅ Supprimé: {var}")

    print("✅ Variables système nettoyées")

    # Vérifier OpenAI
    print("\n🤖 Test OpenAI après nettoyage")
    print("-" * 35)

    try:
        import openai
        print(f"✅ OpenAI version: {openai.__version__}")

        # Test de création du client
        client = openai.OpenAI()
        print("✅ Client OpenAI créé avec succès")

    except Exception as e:
        print(f"❌ Erreur OpenAI: {e}")
        return False

    return True

def set_optimal_environment():
    """Configure l'environnement optimal pour OpenAI"""
    print("\n⚙️  Configuration de l'environnement optimal")
    print("-" * 45)

    # Désactiver les warnings SSL si nécessaire
    os.environ['PYTHONWARNINGS'] = 'ignore::urllib3.exceptions.InsecureRequestWarning'

    # Forcer l'utilisation de TLS 1.2+
    os.environ['OPENSSL_CONF'] = '/dev/null'  # Sur Linux/Mac

    print("✅ Variables d'environnement optimisées")

if __name__ == '__main__':
    print("🚀 Nettoyage de l'environnement pour OpenAI\n")

    # Nettoyer les proxies
    success = clean_proxy_environment()

    # Configurer l'environnement
    set_optimal_environment()

    print("\n" + "=" * 50)

    if success:
        print("✅ Environnement nettoyé avec succès !")
        print("🎯 OpenAI devrait maintenant fonctionner correctement.")
        print("\n💡 Lancez maintenant:")
        print("   python manage.py runserver")
    else:
        print("❌ Problème détecté lors du nettoyage.")
        print("\n🔧 Solutions alternatives:")
        print("1. pip install openai==0.28.1  # Version ancienne")
        print("2. Vérifier les variables d'environnement système")
        print("3. Redémarrer l'ordinateur")
        sys.exit(1)

    print("\n🎉 Prêt pour tester l'IA !")
