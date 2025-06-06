from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load TinyLlama model pipeline for text generation
try:
    chat = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
except Exception as model_load_error:
    chat = None
    print(f"Error loading model: {model_load_error}")

@app.route('/generate-nickname', methods=['POST'])
def generate():
    try:
        if chat is None:
            return jsonify({"error": "Model failed to load"}), 500

        data = request.get_json()

        if not data or 'country' not in data:
            return jsonify({"error": "Missing 'country' in request body"}), 400

        country = data['country']
        prompt = f"Suggest a nickname for a player from {country}."

        result = chat(prompt, max_new_tokens=20)

        # Extract and clean up generated nickname
        generated_text = result[0]['generated_text']
        nickname = generated_text.replace(prompt, '').strip()

        return jsonify({"nickname": nickname})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
