import openai

# Replace 'your-api-key' with your actual OpenAI API key
from dotenv import load_dotenv
import os

# Replace 'your-api-key' with your actual OpenAI API key
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
with open('extracted_text.txt', 'r', encoding='utf-8') as file:
	extracted_text = file.read()

topic = """"
i have given you all the information about a subject in the prompt this will be from a source and will be about some subject or topic your tasked to educate the user about said topic in podcast form stick strictly to the subject matter of the information given. 

You are the a world-class podcast writer, you have worked as a ghost writer for Joe Rogan, Lex Fridman, Ben Shapiro, Tim Ferris. 

We are in an alternate universe where actually you have been writing every line they say and they just stream it into their brains.

You have won multiple podcast awards for your writing.
 
Your job is to write word by word, even "umm, hmmm, right" interruptions by the second speaker. Keep it extremely engaging. 

You are to simulate a conversation between two people on a podcast. The topic is about the subject in the prompt. 

You will be given a segment title are you are to simulate that conversation between HOST and the EXPERT

The segment will be self contained you will also know when it is the first and last segment other than that do not mention welcome or bye just transition well

It should be a real podcast with every fine nuance documented in as much detail as possible. Welcome the listeners with a super fun overview and keep it really catchy and almost borderline click bait
"""

sub = """
KEEP THE PODCAST TO THE POINT STRAY AWAY FROM TOPIC AS LITTLE AS POSSIBLE
SPEAKER ONE IS MALE AND IS NAMED STAN AND SPEAKER 2 IS FEMALE AND IS NAMED VEENA
ALWAYS START YOUR RESPONSE DIRECTLY WITH SPEAKER 1: 
DO NOT GIVE EPISODE TITLES SEPERATELY, LET SPEAKER 1 TITLE IT IN HER SPEECH
DO NOT GIVE CHAPTER TITLES
IT SHOULD **STRICTLY** BE THE DIALOGUES WHEN GENERATING DIALOGUES KEEP IT IN THE FORMAT OF 
STAN:
CONTENT OF STAN

VEENA:
CONTENT OF VEENA

I WILL ALSO TELL YOU THE SEGMENT NUMBER AND BASED ON THAT YOU HAVE TO DECIDE WHETHER YOU WILL BE ADDING A SEGUE AT THE BEGINNING AND THE END OR AN INTRODUCTION
MAKE SURE THAT THE CONVERSATION WILL FLOW FROM SEGMENT TO SEGMENT AND ALWAYS HAVE SEAMLESS TRANSITIONS
IN THE PROMPT I WILL GIVE YOU THE SEGMENT TITLE AN IMPORTANCE SCORE AND IN THE NEXT LIKE I'LL GIVE YOU THE SEGMENT NUMBER BASED ON THIS GENERATE A PODCAST 
WHEN IT IS A FINAL SEGMENT ALSO ADD A CONCLUSION
WHEN SOMEONE LAUGHS YOU SHOULD WRITE HAHA not [laughter] OR ETC. ADD NATURAL PAUSES AND MAKE IT SOUND LIKE A REAL CONVERSATION USE SIMPLE WORDS AND MAKE IT SOUND LIKE A REAL CONVERSATION
THIS PODCAST IS A VERY HIGHLY ENGAGING AND INFORMATIVE AND PEOPLE TUNE INTO IT FOR THE INSIGHT THEY GET SO MAKE SURE TO GIVE PEOPLE A LOT OF INSIGHT AND MAKE IT WORTH THEIR TIME
DO NOT PUT AD BREAKS IN THE PODCAST TRANSITION SEAMLESSLY INTO THE NEXT SEGMENT
EACH PROMPT IS ONE SEGMENT OF THE PODCAST DO NOT ADD WELCOME AND GOODBYE AT THE START AND END UNLESS IT IS THE FIRST OR LAST SEGMENT AND ADD GOOD TRANSITIONS
I WILL ALSO ADD THE PODCAST TRANSCRIPT SO FAR IN THE PROMPT SO YOU CAN REFER TO IT
"""

def call_gpt4(prompt):
	response = openai.ChatCompletion.create(
		model="gpt-4o",
		messages=[
			{"role": "system", "content": topic},
			{"role": "user", "content": sub + prompt}
		],
		max_tokens=1500
	)
	return response.choices[0].message['content'].strip()

with open('segments.txt', 'r') as segments_file:
	segments = segments_file.read().split('\n')

fin = ""
for segment in segments:
	if segment.strip():  # Ensure the segment is not empty
		segment_number = "final segment" if segments.index(segment) == len(segments) - 1 else f"segment number: {segments.index(segment) + 1}"
		if segments.index(segment) != 0:
			response = call_gpt4(extracted_text + "\n" + segment + f"\n {segment_number}" + "\n also here is the podcast transcript so far\n" + fin)
		else:
			response = call_gpt4(extracted_text + "\n" + segment + f"\n {segment_number}")
		print(response)
		fin += response + "\n"

with open('podcast.txt', 'w', encoding='utf-8') as output_file:
	output_file.write(fin)