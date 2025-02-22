from wyoming.client import AsyncTcpClient
from wyoming.tts import Synthesize, SynthesizeVoice
from wyoming.audio import AudioChunk
from wyoming.info import Describe
import wave
import io

class WyomingClient:
    def __init__(self, host="localhost", port=10200):
        self.host = host
        self.port = port

    async def __aenter__(self):
        self.client = AsyncTcpClient(self.host, self.port)
        await self.client.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.disconnect()

async def list_voices(host="localhost", port=10200):
    voices = []
    async with WyomingClient(host, port) as w:
        await w.client.write_event(Describe().event())

        while True:
            event = await w.client.read_event()
            if event.type == "info":
                for tts in event.data.get("tts", []):
                    if not tts:
                        break
                    voices.extend(tts.get('voices', []))
                break
    return voices

async def get_tts(text, voice=None, host="localhost", port=10200):
    audio_bytes = bytes()
    format_info = {
    }
    async with WyomingClient(host, port) as w:

        await w.client.write_event(Synthesize(
            text=text,
            voice=SynthesizeVoice(name=voice)
            ).event())

        while True:
            event = await w.client.read_event()
            if event.type == "audio-start":
                if hasattr(event, 'data'):
                    if 'rate' in event.data:
                        format_info['sample_rate'] = event.data['rate']
                    if 'width' in event.data:
                        format_info['sample_width'] = event.data['width']
                    if 'channels' in event.data:
                        format_info['channels'] = event.data['channels']

            if event.type == "audio-chunk":
                chunk = AudioChunk.from_event(event)
                audio_bytes += chunk.audio
            elif event.type == "audio-stop":
                break

    return audio_bytes, format_info

def audio_to_wav_bytes(audio_bytes, format_info):
    wav_buffer = io.BytesIO()
    
    with wave.open(wav_buffer, "wb") as wav_file:
        wav_file.setnchannels(format_info['channels'])
        wav_file.setsampwidth(format_info['sample_width'])
        wav_file.setframerate(format_info['sample_rate'])
        wav_file.writeframes(audio_bytes)
    
    wav_buffer.seek(0)
    wav_bytes = wav_buffer.getvalue()
    
    return wav_bytes
