from google import genai
from dotenv import load_dotenv
import PIL.Image
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

def ocr_extraction(image_file):
    api_key = os.getenv("API_KEY_EXTRACTION")
    if not api_key:
        return "Error: API_KEY_EXTRACTION not found in environment variables."

    try:
        client = genai.Client(api_key=api_key)
        img = PIL.Image.open(image_file)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        prompt = "Extract the patient name, doctor name, and a list of all medications with their dosages from this prescription."
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, img]
        )
        return response.text

    except Exception as e:
        return f"Error during extraction: {e}"