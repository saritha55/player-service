from flask import Flask, request, jsonify
from transformers import pipeline
import random
import re

app = Flask(__name__)

# Load the model
chat = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

# Fallback nickname list
fallback_nicknames = [
    "Ace", "Blaze", "Shadow", "Bolt", "Rogue", "Viper", "Storm",
    "Ghost", "Maverick", "Nitro", "Spartan", "Venom", "Cyclone",
    "Phoenix", "Striker", "Flash", "Dragon", "Raptor", "Glitch"
]

def clean_nickname(text, prompt, country):
    # Remove the prompt from generated text
    nickname = text.replace(prompt, "").strip()

    # Remove digits and anything not alphabetic
    nickname = re.sub(r"\d+", "", nickname)
    nickname = re.sub(r"[^\w\s]", "", nickname)
    
    # Remove country name if it appears
    nickname = re.sub(re.escape(country), "", nickname, flags=re.IGNORECASE)

    # Remove common bad outputs
    blacklist = ["nickname", "name", "from", "player", "example", "e.g."]
    for word in blacklist:
        nickname = re.sub(rf"\b{word}\b", "", nickname, flags=re.IGNORECASE)

    # Keep only first 2 words if needed
    words = nickname.strip().split()
    nickname = ' '.join(words[:2]) if words else ""

    return nickname.strip()

@app.route('/generate-nickname', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        country = data.get("country", "").strip()

        if not country:
            return jsonify({"error": "Missing 'country' in request"}), 400

        # Refined prompt
        prompt = f"Suggest one cool short nickname for a gamer from {country}: "
        output = chat(prompt, max_new_tokens=20, do_sample=True)[0]["generated_text"]

        nickname = clean_nickname(output, prompt, country)

        if not nickname or len(nickname) < 2:
            nickname = random.choice(fallback_nicknames)

        return jsonify({"nickname": nickname})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
