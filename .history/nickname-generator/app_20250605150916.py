from flask import Flask, request, jsonify
from transformers import pipeline
import re

app = Flask(__name__)

# Load TinyLlama model pipeline for text generation
generator = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

def clean_nickname(text, prompt):
    # Remove the original prompt from the generated text
    nickname = text.replace(prompt, "").strip()

    # Keep only ASCII characters
    nickname = re.sub(r"[^\x00-\x7F]+", "", nickname)
    nickname = re.sub(r"[^\w\s]", "", nickname)

    # Split into words and filter out generic or useless ones
    words = nickname.split()
    blacklist = {"example", "examples", "nickname", "name", "player", "suggestion", "cool"}

    for word in words:
        cleaned = word.strip().capitalize()
        if cleaned.lower() not in blacklist and len(cleaned) > 2:
            return cleaned

    # Fallback if nothing usable
    return "PlayerX"

@app.route('/generate-nickname', methods=['POST'])
def generate_nickname():
    try:
        data = request.get_json()
        country = data.get("country", "")

        if not country:
            return jsonify({"error": "Missing 'country' in request"}), 400

        prompt = f"Suggest a one-word cool English nickname for a player from {country}."
        result = generator(prompt, max_new_tokens=30, num_return_sequences=1)
        raw_text = result[0]["generated_text"]
        nickname = clean_nickname(raw_text, prompt)

        return jsonify({"nickname": nickname})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Device set to use cpu")
    app.run(host="0.0.0.0", port=5000)
