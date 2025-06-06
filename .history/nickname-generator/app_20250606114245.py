from flask import Flask, request, jsonify
from transformers import pipeline
import re
import random

app = Flask(__name__)

# Load the model
generator = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

# Country-specific fallback nicknames
fallback_nicknames = {
    "india": ["Tiger", "Bolt", "Yodha", "Cobra", "Flash"],
    "canada": ["Maple", "Blizzard", "Moose", "Drake", "Frost"],
    "america": ["Blaze", "Ranger", "Eagle", "Ace", "Maverick"],
    "london": ["Knight", "Foggy", "Thames", "Royal", "Storm"],
    "thailand": ["Bang", "Lotus", "Chi", "Storm", "Swift"],
    "china": ["Dragon", "Zen", "Silk", "Phoenix", "Jade"],
    "vietnam": ["Blade", "Bamboo", "Echo", "Strike", "Shadow"],
    "japan": ["Shinobi", "Katana", "Ryu", "Nova", "Shadow"]
}

# Generic fallback if country not found
default_fallback = ["PlayerX", "Blaze", "Storm", "Flash", "Rogue"]

def clean_nickname(text, prompt):
    """Clean and return a valid one-word English nickname without numbers or symbols."""
    nickname = text.replace(prompt, "").strip()
    nickname = re.sub(r"[^\x00-\x7F]+", "", nickname)  # Remove non-ASCII
    nickname = re.sub(r"[^\w\s]", "", nickname)        # Remove special characters
    nickname = re.sub(r"\d+", "", nickname)            # Remove digits

    words = nickname.split()
    blacklist = {"example", "examples","this", "nickname", "name", "player", "suggestion", "cool", "generate", "from"}

    for word in words:
        cleaned = word.strip().capitalize()
        if cleaned.isalpha() and cleaned.lower() not in blacklist and len(cleaned) > 2:
            return cleaned

    return None

@app.route('/generate-nickname', methods=['POST'])
def generate_nickname():
    try:
        data = request.get_json()
        country = data.get("country", "").lower().strip()

        if not country:
            return jsonify({"error": "Missing 'country' in request"}), 400

        prompt = f"Suggest a one-word cool English nickname for a player from {country}."
        result = generator(prompt, max_new_tokens=30, num_return_sequences=1)
        raw_text = result[0]["generated_text"]
        nickname = clean_nickname(raw_text, prompt)

        if nickname:
            return jsonify({"nickname": nickname})
        else:
            # Fallback nickname
            options = fallback_nicknames.get(country, default_fallback)
            return jsonify({"nickname": random.choice(options)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Device set to use cpu")
    app.run(host="0.0.0.0", port=5000)
