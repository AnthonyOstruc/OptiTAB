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