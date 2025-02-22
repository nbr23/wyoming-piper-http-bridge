# wyoming-piper-http-bridge

A quick and dirty bridge to reach piper through the wyoming protocol via HTTP

## Usage

Run it with `uvicorn tts-api:main`

### Text to speech

`curl -X POST -H "Content-Type: application/json" -d '{"text": "happy text to speaching!"}' http://localhost:8000/api/tts | mpv -`