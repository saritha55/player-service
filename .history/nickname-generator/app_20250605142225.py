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

    prompt = f"Generate a single cool nickname for a player from {country}. Only output the nickname."

    output = chat(prompt, max_new_tokens=20)[0]['generated_text']

    # Remove the prompt from the output to get just the nickname part
    nickname = output.replace(prompt, '').strip()

    # Optionally, cut nickname at first period or newline for clean short output
    for sep in ['.', '\n']:
        if sep in nickname:
            nickname = nickname.split(sep)[0].strip()
            break

    return jsonify({"nickname": nickname})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
