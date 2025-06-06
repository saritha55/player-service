from flask import Flask, request, jsonify
from transformers import pipeline
import random
import re

app = Flask(__name__)

chat = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

fallback_nicknames = [
    "Ace", "Flash", "Blaze", "Rocket", "Shadow", "Maverick", "Phoenix",
    "Viper", "Falcon", "Storm", "Dragon", "Wolf", "Rogue", "Titan", "Bolt",
    "Ghost", "Cyclone", "Hawk", "Thunder", "Jaguar", "Raptor", "Spartan",
    "Venom", "Blitz", "Nitro", "Rebel", "Saber", "Tornado"
]

def clean_nickname(text, prompt):
    nickname = text[len(prompt):].strip()

    # Remove special characters, formatting, and quotes
    nickname = re.sub(r"[`\-•\"\'\n\r\t]", '', nickname)
    nickname = re.sub(r'[^a-zA-Z0-9 ]', '', nickname)
    nickname = nickname.strip()

    # Limit to 1-2 words
    words = nickname.split()
    nickname = ' '.join(words[:2]) if words else ''

    return nickname

@app.route('/generate-nickname', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        country = data.get('country', '').strip()

        if not country:
            return jsonify({"error": "Missing 'country' field"}), 400

        prompt = f"Nickname for a player from {country}: "

        output = chat(prompt, max_new_tokens=15, do_sample=True)[0]['generated_text']
        nickname = clean_nickname(output, prompt)

        if len(nickname) < 2 or any(x in nickname.lower() for x in ["nickname", "example", "player", "ensure"]):
            nickname = random.choice(fallback_nicknames)

        return jsonify({"nickname": nickname})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
