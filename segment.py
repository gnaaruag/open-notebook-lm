import openai
from dotenv import load_dotenv
import os

# Replace 'your-api-key' with your actual OpenAI API key
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

with open('extracted_text.txt', 'r', encoding='utf-8') as file:
	extracted_text = file.read()

def call_gpt4(prompt):
	response = openai.ChatCompletion.create(
		model="gpt-4o",
		messages=[
			{"role": "system", "content": "You are a world renowned writer you will be given some research or book or pdf. The user wants to conduct a podcast, you are to help identify few important segments that can be done in the podcast"},
			{"role": "user", "content": prompt}
		],
		# temperature=0.0
	)
	return response.choices[0].message['content'].strip()

# Example usage
custom_prompt = "I am giving you all the contents about a topic can be a book or any document, I want to conduct a podcast between two people can you read this info and tell me the most important topics i can use for my segments each in new line1 i can have on this podcast (give me a minimum of 3 and a max of 6) also only give me names of these segments nothing else. Also make sure that these segments should be interesting and useful for a listener" + extracted_text
response = call_gpt4(custom_prompt)
print(response)
with open('segments.txt', 'w') as output_file:
	output_file.write(response)