from flask import Flask, request, jsonify
from transformers import pipeline
import random

app = Flask(__name__)

# Load TinyLlama model pipeline for text generation
chat = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

fallback_nicknames = [
    "Ace", "Flash", "Blaze", "Rocket", "Shadow", "Maverick", "Phoenix",
    "Viper", "Falcon", "Storm", "Dragon", "Wolf", "Rogue", "Titan", "Bolt",
    "Crusher", "Ghost", "Cyclone", "Hawk", "Thunder", "Jaguar", "Raptor",
    "Spartan", "Venom", "Blitz", "Nitro", "Rebel", "Saber", "Tornado"
]

@app.route('/generate-nickname', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        country = data.get('country', '').strip()

        if not country:
            return jsonify({"error": "Missing 'country' field"}), 400

        prompt = (
            f"Nickname:\n"
            f"Generate ONE unique, creative nickname for a player from {country}.\n"
            f"Output ONLY the nickname (one or two words), no explanation or extra text."
        )

        output = chat(prompt, max_new_tokens=30)[0]['generated_text']

        # Remove the prompt part from output
        nickname = output[len(prompt):].strip()

        # Clean punctuation or quotes around nickname
        nickname = nickname.strip(' "\'.')

        # Fallback if output looks like instructions instead of nickname
        if len(nickname) < 2 or any(
            word in nickname.lower() 
            for word in ["ensure", "nickname", "player", "provide", "output"]
        ):
            nickname = random.choice(fallback_nicknames)

        return jsonify({"nickname": nickname})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
