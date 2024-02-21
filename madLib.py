##
# @description: This program uses the OpenAI API to create a custom madLib story.
# @author Nathan Yan
##

#importing neeeded libraries
import openai
from openai import OpenAI
from pathlib import Path


#OpenAI API key
client = OpenAI(api_key = "API_KEY")

#The type of story the user wants to create
typeOfStory = input("What type of story do you want? Ex.'a story about a fish.'")

#Prompt merged with the type of story
message = f'''
    Write me {typeOfStory}. 
    The story should be less than 300 characters long and should have at 
    least 5 sentences. Make sure the story is interchangeable as it is a madlib.
    In those sentences, there should be at least 2 characters, two verbs, one 
    ing-verb, and three adjectives. In the story, replace TWO verbs as the word 
    [VERB]. These verbs should be regular verbs. Replace one ING verb as 
    [VERB-ING]. Replace THREE adjectives as the word [ADJECTIVE] and replace ONLY 
    TWO words as [CHARACTER]. These two words should be characters and no other 
    characters should be used. Instead, use pronouns to refer to characters in 
    the story. Do not replace any other words.
'''

#Creating the story using the OpenAI API
completion = client.chat.completions.create(
    model="gpt-4", 
    messages=[{
        "role": "user", 
        "content": message
        }])
story = completion.choices[0].message.content


#Replacing the words in the story with user input
countv = 0
counta = 0
countc = 0
counti = 0
for i in range(0, len(story)):
    if "[VERB-ING]" in story:
        if counti == 1:
            pass
        else:
            counti+=1
            verbing = input("Enter a verb ending in -ing: ")
            story = story.replace("[VERB-ING]", verbing, counti)
    if "[VERB]" in story:
        if countv == 2:
            pass
        else:
            countv+=1
            verb = input("Enter a verb: ")
            story = story.replace("[VERB]", verb, countv)
    if "[CHARACTER]" in story:
        if countc == 2:
             pass
        else: 
            countc+=1
            char = input("Enter a character: ")
            story = story.replace("[CHARACTER]", char, countc)
    if "[ADJECTIVE]" in story:
        if counta == 3:
            pass
        else:
            counta+=1
            adj = input("Enter an adjective: ")
            story = story.replace("[ADJECTIVE]", adj, counta)

#Printing the story
print(story)


#Creating an image and audio file using the OpenAI API - Testing the API for fun
response = client.images.generate(
  model="dall-e-3",
  prompt= story,
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
print(image_url)

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input=story,
)

response.stream_to_file(speech_file_path)
