import google.generativeai as genai
from nltk.tokenize import word_tokenize

from core.interface import GPTEngine
from infra.settings import GOOGLE_API_KEY


class GeminiGPTEngine(GPTEngine):
    def process_text(self, text, prompt):
        tokens = word_tokenize(text)
        processed_text = ' '.join(tokens)

        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')

        response = model.generate_content(prompt % processed_text)
        return response
