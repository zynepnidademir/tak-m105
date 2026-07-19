"""
Bu API key'in erisebildigi Gemini modellerini listeler.
Calistir: python modelleri_listele.py
"""
import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY ortam degiskeni bulunamadi!")

client = genai.Client(api_key=api_key)

print("Bu key ile erisilebilen modeller (generateContent destekleyenler):\n")
for model in client.models.list():
    actions = getattr(model, "supported_actions", None) or []
    if "generateContent" in actions:
        print(f"  - {model.name}")