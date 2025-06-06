from flask import Flask, request, jsonify
from transformers import pipeline
import random
import re

app = Flask(__name__)

chat = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

# Fallback nickname pool
fallback_nicknames = [
    "Ace", "Blaze", "Shadow", "Bolt", "Rogue", "Viper", "Storm",
    "Ghost", "Maverick", "Nitro", "Spartan", "Venom", "Cyclone",
    "Phoenix", "Striker", "Flash", "Dragon", "Raptor", "Glitch"
]

def clean_nickname(text, prompt, country):
    # Remove the prompt from generated text
    nickname = text[len(prompt):].strip()

    # Remove unwanted characters and formatting
    nickname = re.sub(r"[`\-•\"\'\n\r\t]", '', nickname)
    nickname = re.sub(r'[^a-zA-Z0-9 ]', '', nickname)

    # Remove country name if repeated in output
    nickname = re.sub(re.escape(country), '', nickname, flags=re.IGNORECASE)

    # Strip and limit to 2 words max
    words = nickname.strip().split()
    nickname = ' '.join(words[:2]) if words else ''

    return nickname.strip()

@app.route('/generate-nickname', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        country = data.get('country', '').strip()

        if not country:
            return jsonify({"error": "Missing 'country' field"}), 400

        prompt = f"Suggest a cool one-word nickname for a player from {country}:"
        output = chat(prompt, max_new_tokens=15, do_sample=True)[0]['generated_text']

        nickname = clean_nickname(output, prompt, country)

        # Fallback if result is weird or not usable
        if not nickname or len(nickname) < 2 or any(word in nickname.lower() for word in ["nickname", "example", "player", "from", "japan"]):
            nickname = random.choice(fallback_nicknames)

        return jsonify({"nickname": nickname})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
