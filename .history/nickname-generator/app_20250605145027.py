from flask import Flask, request, jsonify
from transformers import pipeline
import random
import re

app = Flask(__name__)

chat = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

fallback_nicknames = [
    "Ace", "Flash", "Blaze", "Rocket", "Shadow", "Maverick", "Phoenix",
    "Viper", "Falcon", "Storm", "Dragon", "Wolf", "Rogue", "Titan", "Bolt",
    "Crusher", "Ghost", "Cyclone", "Hawk", "Thunder", "Jaguar", "Raptor",
    "Spartan", "Venom", "Blitz", "Nitro", "Rebel", "Saber", "Tornado"
]

def clean_nickname(text, prompt):
    # Remove the prompt part from the generated text
    nickname = text[len(prompt):].strip()

    # Remove any line breaks or numbers or bullets
    nickname = re.sub(r'[\n\r]', ' ', nickname)  # remove new lines
    nickname = re.sub(r'^[\d\.\-\s"]+', '', nickname)  # remove leading digits, dots, dashes, quotes
    nickname = re.sub(r'["\']', '', nickname)  # remove quotes inside

    # Take only the first two words max (usually nicknames are short)
    words = nickname.split()
    nickname = ' '.join(words[:2])

    return nickname.strip()

@app.route('/generate-nickname', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        country = data.get('country', '').strip()

        if not country:
            return jsonify({"error": "Missing 'country' field"}), 400

        prompt = f"Give a unique and creative nickname for a player from {country}: "

        output = chat(prompt, max_new_tokens=30, do_sample=True)[0]['generated_text']
        nickname = clean_nickname(output, prompt)

        # Fallback if nickname looks like instructions or too short
        if len(nickname) < 2 or any(
            word in nickname.lower()
            for word in ["example", "player", "nickname", "ensure", "unique"]
        ):
            nickname = random.choice(fallback_nicknames)

        return jsonify({"nickname": nickname})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
