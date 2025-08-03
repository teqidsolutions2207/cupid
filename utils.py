import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

def generate_reply(conversation, tone="flirty"):
    prompt = f"""
You're an expert in dating conversations. Analyze the following chat and suggest a smooth, confident, and {tone} reply.

Chat:
{conversation}

Reply:
"""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=150
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("Error generating reply:", e)
        return "Oops! Couldn't generate a reply right now."
