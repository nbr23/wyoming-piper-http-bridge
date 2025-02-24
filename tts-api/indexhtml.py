INDEX_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TTS Voice Selection</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 20px auto;
            padding: 0 20px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        select, textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        textarea {
            min-height: 150px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <h1>Text-to-Speech</h1>
    <form id="ttsForm">
        <div class="form-group">
            <label for="textInput">Text to speak:</label>
            <textarea id="textInput"></textarea>
        </div>
        
        <div class="form-group">
            <label for="languageSelect">Language:</label>
            <select id="languageSelect"></select>
        </div>
        
        <div class="form-group">
            <label for="voiceSelect">Voice:</label>
            <select id="voiceSelect"></select>
        </div>
        
        <div class="form-group">
            <label for="speakerSelect">Speaker:</label>
            <select id="speakerSelect"></select>
        </div>
        
        <button type="submit">Speak!</button>
        
        <div class="form-group" style="margin-top: 20px;">
            <audio id="audioPlayer" controls style="width: 100%; display: none;"></audio>
        </div>
    </form>

    <script>
        let voices = [];
        
        async function fetchVoices() {
            try {
                const response = await fetch(`${window.location.pathname}api/voices`);
                voices = await response.json();
                initializeForm();
            } catch (error) {
                console.error('Error fetching voices:', error);
            }
        }

        function initializeForm() {
            const languages = [...new Set(voices.flatMap(voice => voice.languages))];
            const languageSelect = document.getElementById('languageSelect');
            languages.forEach(lang => {
                const option = new Option(lang, lang);
                languageSelect.add(option);
            });
            languageSelect.value = 'en_US';
            updateVoiceSelect();
        }

        function updateVoiceSelect() {
            const selectedLanguage = document.getElementById('languageSelect').value;
            const voiceSelect = document.getElementById('voiceSelect');
            
            voiceSelect.innerHTML = '';

            const filteredVoices = voices.filter(voice => 
                voice.languages.includes(selectedLanguage)
            );
            filteredVoices.forEach(voice => {
                const option = new Option(voice.description, voice.name);
                voiceSelect.add(option);
            });
            updateSpeakerSelect();
        }

        function updateSpeakerSelect() {
            const selectedVoice = document.getElementById('voiceSelect').value;
            const speakerSelect = document.getElementById('speakerSelect');
            speakerSelect.innerHTML = '';
            const voice = voices.find(v => v.name === selectedVoice);
            if (voice && voice.speakers && voice.speakers.length > 0) {
                voice.speakers.forEach(speaker => {
                    const option = new Option(speaker.name, speaker.name);
                    speakerSelect.add(option);
                });
                speakerSelect.disabled = false;
            } else {
                speakerSelect.add(new Option('No speakers available', ''));
                speakerSelect.disabled = true;
            }
        }

        document.getElementById('languageSelect').addEventListener('change', updateVoiceSelect);
        document.getElementById('voiceSelect').addEventListener('change', updateSpeakerSelect);

        document.getElementById('ttsForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = {
                text: document.getElementById('textInput').value,
                language: document.getElementById('languageSelect').value,
                voice: document.getElementById('voiceSelect').value,
                speaker: document.getElementById('speakerSelect').value || null
            };

            try {
                const response = await fetch(`${window.location.pathname}api/tts`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                if (!response.ok) {
                    throw new Error('Synthesis failed');
                }

                const audioBlob = await response.blob();
                const audioUrl = URL.createObjectURL(audioBlob);
                const audioElement = document.getElementById('audioPlayer');
                audioElement.style.display = 'block';
                audioElement.src = audioUrl;
                await audioElement.play();
                audioElement.onended = () => {
                    URL.revokeObjectURL(audioUrl);
                };
            } catch (error) {
                console.error('Error during synthesis request:', error);
            }
        });
        fetchVoices();
    </script>
</body>
</html>
'''