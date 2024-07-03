from openai import OpenAI
import requests
import os
from dotenv import load_dotenv

load_dotenv(".env")
key = os.getenv("KEY")

def get_2d_image(object):
   client = OpenAI(api_key=key)
   respose = client.images.generate(
     model="dall-e-3",
     prompt= f"A simple 2D silhouette of a {object} on a completely plain white background. No frames, borders, textures, or any additional elements.",
     size="1024x1024",
     quality="standard",
     n=1,
   )

   url = respose.data[0].url
   data =  requests.get(url).content
   with open("temp/img.png", "wb") as handler:
       handler.write(data)
   


