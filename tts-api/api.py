from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from .wyoming import list_voices, get_tts, audio_to_wav_bytes

class TTSApi:
    def __init__(self, piper_host="localhost", piper_port=10200):
        self.piper_host = piper_host
        self.piper_port = piper_port
        self.app = Starlette(debug=True, routes=[
            Route('/api/voices', self.api_list_voices),
            Route('/api/tts', self.api_get_tts, methods=['POST'])
        ])

    async def api_list_voices(self, request):
        voices = await list_voices(self.piper_host, self.piper_port)
        return JSONResponse(voices)

    async def api_get_tts(self, request):
        data = await request.json()
        text = data.get('text')
        voice = data.get('voice')
        audio_bytes, format_info = await get_tts(text, voice, self.piper_host, self.piper_port)
        return Response(audio_to_wav_bytes(audio_bytes, format_info), media_type='audio/wav')