from flask import Flask, request, jsonify
from transformers import pipeline
import re

app = Flask(__name__)

# Load the text generation model (e.g., TinyLlama)
generator = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

def clean_nickname(text, prompt):
    # Remove the prompt from generated output
    nickname = text.replace(prompt, "").strip()

    # Keep only ASCII characters (English), remove punctuation
    nickname = re.sub(r"[^\x00-\x7F]+", "", nickname)  # remove non-English chars
    nickname = re.sub(r"[^\w\s]", "", nickname)        # remove punctuation

    # Split by space and return only the first word
    nickname = nickname.split()[0] if nickname else "PlayerX"

    return nickname

@app.route('/generate-nickname', methods=['POST'])
def generate_nickname():
    try:
        data = request.get_json()
        country = data.get('country', '').strip()

        if not country:
            return jsonify({'error': 'Missing "country" in request'}), 400

        prompt = f"Suggest a cool one-word English nickname for a player from {country}:"
        result = generator(prompt, max_new_tokens=30, num_return_sequences=1)
        generated_text = result[0]['generated_text']
        nickname = clean_nickname(generated_text, prompt)

        return jsonify({'nickname': nickname})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
