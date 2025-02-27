from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response, HTMLResponse
from starlette.routing import Route
from .indexhtml import INDEX_HTML

from .wyoming import list_voices, get_tts, audio_to_wav_bytes

class TTSApi:
    def __init__(self, piper_host="localhost", piper_port=10200):
        self.piper_host = piper_host
        self.piper_port = piper_port
        self.app = Starlette(debug=True, routes=[
            Route('/api/voices', self.api_list_voices),
            Route('/api/tts', self.api_get_tts, methods=['POST', 'GET']),
            Route('/', lambda request: HTMLResponse(INDEX_HTML)),
        ])

    async def api_list_voices(self, request):
        language = request.query_params.get('language')
        voices = await list_voices(host=self.piper_host, port=self.piper_port)
        if language:
            res = []
            for voice in voices:
                for lang in voice.get('languages', []):
                    if lang == language:
                        res.append(voice)
            return JSONResponse(res)
        return JSONResponse(voices)

    async def api_get_tts(self, request):
        post_data = {}
        if request.method == 'POST':
            post_data = await request.json()
        get_data = request.query_params
        data = {**get_data, **post_data}

        text = data.get('text')
        voice = data.get('voice')
        language = data.get('language')
        speaker = data.get('speaker')
        speed = float(data.get('speed', 1.0))

        audio_bytes, format_info = await get_tts(text, voice=voice, language=language, speaker=speaker, host=self.piper_host, port=self.piper_port)
        return Response(audio_to_wav_bytes(audio_bytes, format_info, speed=speed), media_type='audio/wav')