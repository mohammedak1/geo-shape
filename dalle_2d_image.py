from openai import OpenAI
import requests
client = OpenAI(api_key="sk-proj-HYkTOHk65zjqu6PAugtwT3BlbkFJVv9EA1PGvkGMNJJEo5TD")

def get_2d_image(object):
   respose = client.images.generate(
     model="dall-e-3",
     prompt= f"A simple 2D drawing of {object}, with minimal details, in black color on a white background. The {object} should have basic features and a straightforward silhouette, resembling a canvas sketch with only black and white colors.",
     size="1024x1024",
     quality="standard",
     n=1,
   )

   url = respose.data[0].url
   data =  requests.get(url).content
   with open("temp/img.png", "wb") as handler:
       handler.write(data)
   


