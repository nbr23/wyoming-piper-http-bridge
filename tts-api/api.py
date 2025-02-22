from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from .wyoming import list_voices, get_tts, audio_to_wav_bytes

async def api_list_voices(request):
    voices = await list_voices()
    return JSONResponse(voices)

async def api_get_tts(request):
    data = await request.json()
    text = data.get('text')
    audio_bytes, format_info = await get_tts(text)
    return Response(audio_to_wav_bytes(audio_bytes, format_info), media_type='audio/wav')

app = Starlette(debug=True, routes=[
    Route('/api/voices', api_list_voices),
    Route('/api/tts', api_get_tts, methods=['POST'])
])