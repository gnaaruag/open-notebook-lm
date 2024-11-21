import requests
from pydub import AudioSegment
import io
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

def parse_podcast_script(file_path):
	with open(file_path, 'r', encoding='utf-8') as file:
		lines = file.readlines()

	parsed_lines = []
	current_speaker = None

	for line in lines:
		if line.startswith("STAN:"):
			current_speaker = 1
			line_content = line.replace("STAN:", "").strip()
		elif line.startswith("VEENA:"):
			current_speaker = 2
			line_content = line.replace("VEENA:", "").strip()
		else:
			line_content = line.strip()

		if line_content:
			parsed_lines.append([current_speaker, line_content])

	return parsed_lines

# Example usage
file_path = 'podcast.txt'
parsed_script = parse_podcast_script(file_path)
print(parsed_script)

combined_audio = AudioSegment.empty()

for speaker, text in parsed_script:
	if speaker == 1:
		url = os.getenv("ELEVEN_LABS_AUDIO_1")
	elif speaker == 2:
		url = os.getenv("ELEVEN_LABS_AUDIO_2")
	else:
		continue

	payload = {
		"text": text,
		"model_id": "eleven_multilingual_v2",
		"voice_settings": {
			"stability": 0,
			"similarity_boost": 0.5,
			"style": 1,
			"use_speaker_boost": True
		}
	}
	headers = {
		"xi-api-key": os.getenv("ELEVEN_LABS_API_KEY"),
		"Content-Type": "application/json"
	}

	response = requests.request("POST", url, json=payload, headers=headers)
	audio_segment = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
	combined_audio += audio_segment

timestamp = datetime.now().strftime("%H%M%S%d%m%Y")
file_name = f"{timestamp}.mp3"
combined_audio.export(file_name, format="mp3")