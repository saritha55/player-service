from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load TinyLlama model pipeline for text generation
chat = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

@app.route('/generate-nickname', methods=['POST'])
def generate():
    data = request.get_json()
    country = data.get('country', '').strip()

    if not country:
        return jsonify({"error": "Missing 'country' field"}), 400

    prompt = (
        f"Provide exactly one unique and creative nickname "
        f"for a player from {country}. "
        f"Output only the nickname without any explanation."
    )

    output = chat(prompt, max_new_tokens=20)[0]['generated_text']
    nickname = output.replace(prompt, '').strip()

    # Cut at first punctuation or newline for clean output
    for sep in ['.', '\n']:
        if sep in nickname:
            nickname = nickname.split(sep)[0].strip()
            break

    # If still empty or generic, fallback response
    if not nickname:
        nickname = "PlayerX"

    return jsonify({"nickname": nickname})
