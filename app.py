from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Initialize Flask app
app = Flask(__name__)

# Allow CORS from specific domain
CORS(app, resources={r"/*": {"origins": "https://preview--cupid-chat-ui.lovable.app"}})

# Analyze chat and return a flirty/smooth reply
@app.route("/analyze-chat", methods=["POST"])
def analyze_chat():
    data = request.get_json()
    conversation = data.get("conversation", "")
    tone = data.get("tone", "flirty")

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
        reply = response['choices'][0]['message']['content'].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Could not generate a reply."}), 500

# Generate a pickup line
@app.route("/generate-line", methods=["POST"])
def generate_line():
    data = request.get_json()
    context = data.get("context", "something romantic or quirky")
    tone = data.get("tone", "flirty")

    prompt = f"""
You are a world-class dating coach and comedian. Create a **fresh, original, and clever** pickup line that is {tone}. 

Avoid clichés. Think witty, unexpected, charming, or bold. Include humor or wordplay if appropriate.

Here is the context or keyword for inspiration:
"{context}"

Only return the pickup line without any explanation.
"""

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,  # More creative
            max_tokens=100,
        )
        line = response['choices'][0]['message']['content'].strip()
        return jsonify({"pickup_line": line})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Could not generate a pickup line."}), 500


# Get a dating tip
@app.route("/get-dating-tip", methods=["GET"])
def get_dating_tip():
    prompt = """
You're a dating coach. Give one short, practical, and confident dating tip for online chats.

Dating Tip:
"""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=80
        )
        tip = response['choices'][0]['message']['content'].strip()
        return jsonify({"tip": tip})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Could not fetch a tip."}), 500

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
