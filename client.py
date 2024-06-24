import google.generativeai as genai
import os

genai.configure(api_key='GEMINI_API_KEY')

model = genai.GenerativeModel()
response = model.generate_content('how to use websocket in python')

print(response.text)
