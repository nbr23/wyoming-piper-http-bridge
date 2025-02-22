import os
from .api import TTSApi

piper_host = os.getenv('PIPER_HOST', 'localhost')
piper_port = os.getenv('PIPER_PORT', 10200)

api = TTSApi(piper_host, piper_port)