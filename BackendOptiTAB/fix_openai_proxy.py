#!/usr/bin/env python
"""
Solution radicale pour le problème de proxy OpenAI
"""
import os
import sys

def fix_openai_proxy_issue():
    """Corrige définitivement le problème de proxy OpenAI"""
    print("🔧 Correction radicale du proxy OpenAI")
    print("=" * 45)

    # Nettoyer toutes les variables d'environnement possibles
    proxy_env_vars = [
        'HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy',
        'OPENAI_PROXY', 'ALL_PROXY', 'all_proxy', 'no_proxy', 'NO_PROXY',
        'REQUESTS_CA_BUNDLE', 'SSL_CERT_FILE', 'OPENSSL_CONF',
        'CURL_CA_BUNDLE', 'REQUESTS_PROXY', 'HTTPS_CERT_FILE'
    ]

    cleaned = []
    for var in proxy_env_vars:
        if var in os.environ:
            del os.environ[var]
            cleaned.append(var)
            print(f"🗑️  Supprimé: {var}")

    print(f"\n✅ {len(cleaned)} variables d'environnement nettoyées")

    # Créer un fichier de configuration OpenAI
    config_content = """
# Configuration OpenAI pour éviter les problèmes de proxy
import os
os.environ['OPENAI_PROXY'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''

# Désactiver les warnings SSL
import warnings
warnings.filterwarnings('ignore', message='.*Unverified HTTPS.*')
"""

    config_file = 'openai_config.py'
    with open(config_file, 'w') as f:
        f.write(config_content.strip())

    print("📝 Fichier de configuration créé")

    # Tester OpenAI
    print("\n🤖 Test OpenAI après correction")
    print("-" * 35)

    try:
        # Importer la configuration
        exec(open(config_file).read())

        import openai
        print(f"✅ OpenAI {openai.__version__} importé")

        # Test avec gestion d'erreur spécifique
        try:
            client = openai.OpenAI(api_key="test_key")
            print("✅ Client OpenAI créé avec succès")
            return True
        except TypeError as e:
            if 'proxies' in str(e):
                print("❌ Problème de proxy persistant")
                print("💡 Solution: Redémarrer l'ordinateur complètement")
                return False
            else:
                raise e

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == '__main__':
    success = fix_openai_proxy_issue()
    print("\n" + "=" * 50)
    if success:
        print("✅ Problème de proxy corrigé !")
        print("🎯 Testez maintenant l'IA")
    else:
        print("❌ Problème persistant")
        print("🔧 Solutions:")
        print("1. Redémarrer l'ordinateur")
        print("2. pip uninstall openai && pip install openai==0.28.1")
        print("3. Utiliser un VPN ou changer de réseau")
        sys.exit(1)
